"""
Flask-server för leaderboard och resultathantering.
Sätter upp API-endpoints för att visa leaderboard och ta emot resultat.
"""
import os
import socket
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from flask import Flask, jsonify, request, send_from_directory, session, redirect, url_for, render_template
import db
import competition_loader
import translations
import re

app = Flask(__name__)

# Läs API-nyckel från miljövariabel
API_KEY = os.getenv("API_KEY", "default_secret_key_change_me")

# Sätt session secret key
app.secret_key = os.getenv("SECRET_KEY", "change_this_secret_key_in_production")

# Load competitions dynamically from folder structure
COMPETITIONS = competition_loader.load_competitions()


def get_current_language():
    """Get current language from session, default to Swedish."""
    return session.get('language', 'sv')


def t(category, key, *args):
    """Helper function to get translated string for current language."""
    lang = get_current_language()
    return translations.t(lang, category, key, *args)


def markdown_to_html(text):
    """Simple markdown to HTML converter for Summary.md content."""
    if not text:
        return ""
    
    lines = text.split('\n')
    result_lines = []
    in_list = False
    in_paragraph = False
    current_paragraph = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Handle headers (### Level X: Title)
        if stripped.startswith('### '):
            # Close any open paragraph or list
            if in_paragraph:
                result_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
                in_paragraph = False
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            
            header_text = stripped[4:].strip()
            # Convert bold in headers
            header_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', header_text)
            result_lines.append(f'<h3>{header_text}</h3>')
        
        # Handle bullet lists
        elif stripped.startswith('- '):
            # Close any open paragraph
            if in_paragraph:
                result_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
                in_paragraph = False
            
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            
            list_item = stripped[2:].strip()
            # Convert bold in list items
            list_item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', list_item)
            result_lines.append(f'<li>{list_item}</li>')
        
        # Handle regular paragraphs
        elif stripped:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            
            # Convert bold in paragraphs
            processed_line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            current_paragraph.append(processed_line)
            in_paragraph = True
        
        # Handle empty lines (end paragraph)
        else:
            if in_paragraph:
                result_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
                in_paragraph = False
            if in_list:
                result_lines.append('</ul>')
                in_list = False
        
        i += 1
    
    # Close any remaining open structures
    if in_paragraph:
        result_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
    if in_list:
        result_lines.append('</ul>')
    
    return '\n'.join(result_lines)


@app.template_filter('markdown')
def markdown_filter(text):
    """Jinja2 filter for markdown conversion."""
    return markdown_to_html(text)


@app.context_processor
def inject_competition_data():
    """Makes competition data, max_level, and translations available to all templates."""
    lang = get_current_language()
    translations_dict = translations.get_translations(lang)
    
    try:
        competition_id = db.get_active_competition_id()
        if competition_id and competition_id in COMPETITIONS:
            competition = COMPETITIONS[competition_id]
            max_level = max(competition["levels"].keys()) if competition["levels"] else 0
            return {
                "competition": competition,
                "max_level": max_level,
                "competition_id": competition_id,
                "t": lambda category, key, *args: translations.t(lang, category, key, *args),
                "translations": translations_dict,
                "current_lang": lang
            }
    except Exception:
        pass
    
    # Default values if no competition is available
    return {
        "competition": None,
        "max_level": 0,
        "competition_id": None,
        "t": lambda category, key, *args: translations.t(lang, category, key, *args),
        "translations": translations_dict,
        "current_lang": lang
    }


@app.route("/set_language/<lang>")
def set_language(lang):
    """Set language preference in session."""
    if lang in ['en', 'sv']:
        session['language'] = lang
    # Redirect back to the page that called this, or to index
    return redirect(request.referrer or url_for('index'))


@app.route("/")
def index():
    """Huvudsida - omdirigera till login eller leaderboard."""
    if 'username' in session:
        return redirect(url_for('leaderboard'))
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login-sida för användare."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username and username.isalnum():
            session['username'] = username
            # Redirect to competition intro instead of directly to level 1
            competition_id = db.get_active_competition_id()
            if competition_id and competition_id in COMPETITIONS:
                return redirect(url_for('competition_intro'))
            else:
                return redirect(url_for('leaderboard'))
        else:
            return render_template('login.html', error=t('login', 'error_invalid_username'))
    
    return render_template('login.html')


@app.route("/logout")
def logout():
    """Loggar ut användaren."""
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route("/level/<int:level_id>")
def level(level_id):
    """Visar problem för en specifik nivå."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if level_id < 1:
        return redirect(url_for('leaderboard'))
    
    username = session['username']
    competition_id = db.get_active_competition_id()
    
    # Kontrollera att tävlingen finns
    if not competition_id or competition_id not in COMPETITIONS:
        return redirect(url_for('leaderboard'))
    
    competition = COMPETITIONS[competition_id]
    
    # Kontrollera att nivån finns i tävlingen
    if level_id not in competition["levels"]:
        return redirect(url_for('leaderboard'))
    
    # Kontrollera att alla tidigare nivåer är klara (förutom nivå 1)
    if level_id > 1:
        # Kontrollera om alla nivåer 1 till level_id-1 är klara
        for prev_level in range(1, level_id):
            if prev_level not in competition["levels"]:
                continue
            if not db.has_completed_level(username, competition_id, prev_level):
                # Hitta första oklara nivå och omdirigera dit
                return redirect(url_for('level', level_id=prev_level))
    
    problem = competition["levels"][level_id]
    
    return render_template('level.html', problem=problem, level_id=level_id, username=username, competition_id=competition_id)


@app.route("/submit/<int:level_id>", methods=['POST'])
def submit(level_id):
    """Hanterar svar för en nivå."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if level_id < 1:
        return redirect(url_for('leaderboard'))
    
    username = session['username']
    competition_id = db.get_active_competition_id()
    
    # Kontrollera att tävlingen finns
    if not competition_id or competition_id not in COMPETITIONS:
        return redirect(url_for('leaderboard'))
    
    competition = COMPETITIONS[competition_id]
    
    # Kontrollera att nivån finns i tävlingen
    if level_id not in competition["levels"]:
        return redirect(url_for('leaderboard'))
    
    problem = competition["levels"][level_id]
    
    # Kontrollera att tävlingen är aktiv
    competition_state = db.get_competition_state(competition_id)
    if not competition_state.get("is_active", False):
        return render_template('level.html', 
                             problem=problem, 
                             level_id=level_id, 
                             username=username,
                             competition_id=competition_id,
                             error=t('errors', 'competition_not_active'))
    
    answer = request.form.get('answer', '').strip()
    if not answer:
        return render_template('level.html', 
                                 problem=problem, 
                                 level_id=level_id, 
                                 username=username,
                                 competition_id=competition_id,
                                 error=t('errors', 'answer_required'))
    
    # Validera svar med expected_answer från competition config
    expected_answer = problem.get("expected_answer", "")
    input_type = problem.get("input_type", "text")
    is_correct = db.submit_answer(username, competition_id, level_id, answer, expected_answer, input_type)
    
    if is_correct:
        # Bestäm nästa nivå eller leaderboard
        max_level = max(competition["levels"].keys())
        if level_id < max_level:
            next_level = level_id + 1
            next_url = url_for('level', level_id=next_level)
        else:
            next_level = None
            next_url = url_for('leaderboard')
        
        return render_template('level.html', 
                             problem=problem, 
                             level_id=level_id, 
                             username=username,
                             competition_id=competition_id,
                             success=True,
                             next_url=next_url,
                             next_level=next_level)
    else:
        return render_template('level.html', 
                             problem=problem, 
                             level_id=level_id, 
                             username=username,
                             competition_id=competition_id,
                             error=t('errors', 'wrong_answer'))


@app.route("/competition/intro")
def competition_intro():
    """Visar tävlingsintroduktion med Summary.md innehåll."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    competition_id = db.get_active_competition_id()
    
    # Kontrollera att tävlingen finns
    if not competition_id or competition_id not in COMPETITIONS:
        return redirect(url_for('leaderboard'))
    
    competition = COMPETITIONS[competition_id]
    summary = competition.get("summary")
    
    return render_template('competition_intro.html', 
                         competition=competition,
                         summary=summary,
                         competition_id=competition_id)


@app.route("/leaderboard")
def leaderboard():
    """Visar leaderboard."""
    leaderboard_data = db.load_leaderboard()
    competition_id = db.get_active_competition_id()
    max_level = 0
    if competition_id and competition_id in COMPETITIONS:
        competition = COMPETITIONS[competition_id]
        max_level = max(competition["levels"].keys()) if competition["levels"] else 0
    return render_template('leaderboard.html', leaderboard=leaderboard_data, max_level=max_level)


@app.route("/api/leaderboard")
def api_leaderboard():
    """Returnerar leaderboard som JSON."""
    leaderboard_data = db.load_leaderboard()
    competition_id = db.get_active_competition_id()
    max_level = 0
    if competition_id and competition_id in COMPETITIONS:
        competition = COMPETITIONS[competition_id]
        max_level = max(competition["levels"].keys()) if competition["levels"] else 0
    # Returnera array för bakåtkompatibilitet, men lägg till max_level i varje entry
    for entry in leaderboard_data:
        entry["max_level_total"] = max_level
    return jsonify(leaderboard_data)


@app.route("/download/<string:competition_id>/<int:level_id>/<filename>")
def download_input_file(competition_id, level_id, filename):
    """
    Laddar ner input-fil för en nivå.
    Säkerhet: Validerar att tävlingen och nivån finns, och att filnamnet matchar.
    """
    # Kontrollera att tävlingen finns
    if competition_id not in COMPETITIONS:
        return t('errors', 'competition_not_found'), 404
    
    competition = COMPETITIONS[competition_id]
    
    # Kontrollera att nivån finns i tävlingen
    if level_id not in competition["levels"]:
        return t('errors', 'level_not_found'), 404
    
    level = competition["levels"][level_id]
    
    # Kontrollera att nivån har en input_file och att filnamnet matchar
    if "input_file" not in level:
        return t('errors', 'no_input_file'), 404
    
    if level["input_file"] != filename:
        return t('errors', 'invalid_filename'), 403
    
    # Säkerhetskontroll: Filnamnet ska inte innehålla path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return t('errors', 'invalid_filename'), 403
    
    # Konstruera sökväg till filen (use folder_name from competition)
    from pathlib import Path
    competitions_dir = Path("competitions")
    file_path = competitions_dir / competition["folder_name"] / f"level{level_id}" / filename
    
    # Ytterligare säkerhetskontroll: Verifiera att filen verkligen finns på rätt plats
    if not file_path.exists() or not file_path.is_file():
        return t('errors', 'file_not_found'), 404
    
    # Verifiera att filen är inom competitions-katalogen (prevent path traversal)
    try:
        file_path.resolve().relative_to(Path("competitions").resolve())
    except ValueError:
        return t('errors', 'invalid_path'), 403
    
    # Servera filen
    directory = str(file_path.parent)
    return send_from_directory(directory, filename, as_attachment=True)


@app.route("/solution/<string:competition_id>/<int:level_id>")
def get_solution(competition_id, level_id):
    """
    Hämtar lösningsprogrammet för en nivå.
    Returnerar solution.py innehållet som text.
    Säkerhet: Validerar att tävlingen och nivån finns.
    """
    # Kontrollera att tävlingen finns
    if competition_id not in COMPETITIONS:
        return t('errors', 'competition_not_found'), 404
    
    competition = COMPETITIONS[competition_id]
    
    # Kontrollera att nivån finns i tävlingen
    if level_id not in competition["levels"]:
        return t('errors', 'level_not_found'), 404
    
    level = competition["levels"][level_id]
    
    # Kontrollera att nivån har en solution file
    if "solution_file" not in level:
        return "Ingen lösning finns för denna nivå", 404
    
    # Konstruera sökväg till solution.py (use folder_name from competition)
    from pathlib import Path
    # Use absolute path based on the script's location to avoid working directory issues
    base_dir = Path(__file__).parent.absolute()
    competitions_dir = base_dir / "competitions"
    solution_path = competitions_dir / competition["folder_name"] / f"level{level_id}" / "solution.py"
    
    # Säkerhetskontroll: Verifiera att filen verkligen finns på rätt plats
    if not solution_path.exists() or not solution_path.is_file():
        return t('errors', 'file_not_found'), 404
    
    # Verifiera att filen är inom competitions-katalogen (prevent path traversal)
    try:
        solution_path.resolve().relative_to(competitions_dir.resolve())
    except ValueError:
        return t('errors', 'invalid_path'), 403
    
    # Läs och returnera filinnehållet
    try:
        with open(solution_path, 'r', encoding='utf-8') as f:
            solution_content = f.read()
        return solution_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return t('errors', 'error_reading_solution', str(e)), 500


@app.route("/admin")
def admin():
    """Admin-kontrollpanel för tävlingsledare."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return t('errors', 'invalid_api_key'), 403
    
    active_competition_id = db.get_active_competition_id()
    competition_state = db.get_competition_state(active_competition_id)
    all_competitions = db.get_all_competitions()
    
    # Lägg till competition info från COMPETITIONS config
    competitions_with_info = []
    for comp in all_competitions:
        comp_id = comp["id"]
        comp_info = COMPETITIONS.get(comp_id, {})
        comp["config"] = comp_info
        comp["is_active"] = (comp_id == active_competition_id)
        competitions_with_info.append(comp)
    
    # Formatera start_time till läsbart format om tävlingen är aktiv
    if competition_state.get("is_active") and competition_state.get("start_time", 0) > 0:
        import datetime
        start_time_ts = competition_state.get("start_time")
        start_time_formatted = datetime.datetime.fromtimestamp(start_time_ts).strftime('%Y-%m-%d %H:%M:%S')
        competition_state["start_time_formatted"] = start_time_formatted
    else:
        competition_state["start_time_formatted"] = None
    
    competition_state["active_competition_id"] = active_competition_id
    
    return render_template('admin.html', state=competition_state, competitions=competitions_with_info)


@app.route("/admin/start", methods=["POST"])
def admin_start():
    """Startar den aktiva tävlingen."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return jsonify({"error": t('errors', 'invalid_api_key_error')}), 403
    
    competition_id = db.get_active_competition_id()
    if not competition_id:
        return jsonify({"error": t('errors', 'no_active_competition')}), 400
    
    import time
    start_time = int(time.time())
    db.set_competition_state(competition_id, True, start_time)
    
    return jsonify({"success": True, "message": t('errors', 'competition_started')})


@app.route("/admin/stop", methods=["POST"])
def admin_stop():
    """Stoppar den aktiva tävlingen."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return jsonify({"error": t('errors', 'invalid_api_key_error')}), 403
    
    competition_id = db.get_active_competition_id()
    if not competition_id:
        return jsonify({"error": t('errors', 'no_active_competition')}), 400
    
    # Behåll start_time när vi stoppar - sätt bara is_active till False
    current_state = db.get_competition_state(competition_id)
    existing_start_time = current_state.get("start_time", 0)
    db.set_competition_state(competition_id, False, existing_start_time)
    
    return jsonify({"success": True, "message": t('errors', 'competition_stopped')})


@app.route("/admin/competitions", methods=["POST"])
def admin_set_active_competition():
    """Sätter aktiv tävling."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return jsonify({"error": t('errors', 'invalid_api_key_error')}), 403
    
    data = request.json
    if not data or "competition_id" not in data:
        return jsonify({"error": t('errors', 'missing_competition_id')}), 400
    
    competition_id = data["competition_id"]
    
    # Kontrollera att tävlingen finns
    if competition_id not in COMPETITIONS:
        return jsonify({"error": t('errors', 'invalid_competition')}), 400
    
    # Sätt som aktiv
    db.set_active_competition(competition_id)
    
    return jsonify({"success": True, "message": t('errors', 'competition_set', competition_id)})


@app.route("/update", methods=["POST"])
def update():
    """
    Tar emot resultat från användare och sparar om det är bättre.
    Förväntar JSON: {"user": str, "level": int, "ms": int}
    """
    data = request.json
    
    if not data or "user" not in data or "level" not in data or "ms" not in data:
        return jsonify({"error": "Missing user, level or ms"}), 400
    
    user = data["user"]
    level = data["level"]
    ms = data["ms"]
    
    # Validera att nivå och tid är positiva
    if not isinstance(level, int) or level < 1:
        return jsonify({"error": t('errors', 'invalid_level')}), 400
    
    if not isinstance(ms, int) or ms < 0:
        return jsonify({"error": t('errors', 'invalid_time')}), 400
    
    competition_id = db.get_active_competition_id()
    
    # Kontrollera att tävlingen är aktiv
    if not competition_id:
        return jsonify({"error": t('errors', 'no_active_competition')}), 400
    
    competition_state = db.get_competition_state(competition_id)
    if not competition_state.get("is_active", False):
        return jsonify({"error": t('errors', 'competition_inactive')}), 403
    
    # Kontrollera att nivån finns i tävlingen
    if competition_id not in COMPETITIONS:
        return jsonify({"error": t('errors', 'competition_not_found')}), 400
    
    if level not in COMPETITIONS[competition_id]["levels"]:
        return jsonify({"error": t('errors', 'level_not_in_competition')}), 400
    
    improved = db.save_result(user, competition_id, level, ms)
    
    return jsonify({
        "success": True,
        "improved": improved,
        "message": t('messages', 'time_improved') if improved else t('messages', 'no_improvement')
    })


@app.route("/reset", methods=["GET"])
def reset():
    """
    Raderar alla resultat. Kräver X-API-Key header.
    """
    api_key_header = request.headers.get("X-API-Key")
    
    if api_key_header != API_KEY:
        return jsonify({"error": t('errors', 'invalid_api_key_error')}), 403
    
    # Radera databasfilen och skapa ny tabell
    import sqlite3
    import os as os_module
    
    if os_module.path.exists(db.DB_PATH):
        os_module.remove(db.DB_PATH)
    
    db.init_db()
    db.init_competitions(COMPETITIONS)
    
    return jsonify({"success": True, "message": t('errors', 'all_data_deleted')})


def get_network_ip():
    """Hämtar serverns nätverks-IP-adress."""
    try:
        # Anslut till en extern adress för att få lokal IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


if __name__ == "__main__":
    # Initiera databas vid start
    db.init_db()
    
    # Initiera tävlingar i databasen
    db.init_competitions(COMPETITIONS)
    
    # Läs host och port från miljövariabler
    flask_host = os.getenv("FLASK_HOST", "0.0.0.0")
    flask_port = int(os.getenv("FLASK_PORT", "5000"))
    
    # Hämta nätverks-IP
    network_ip = get_network_ip()
    
    # Starta Flask-server
    print(f"\n{'='*60}")
    print(f"🚀 Server startar på port {flask_port}")
    print(f"{'='*60}")
    print(f"📍 Lokal åtkomst:")
    print(f"   http://127.0.0.1:{flask_port}/")
    print(f"   http://localhost:{flask_port}/")
    
    if network_ip:
        print(f"\n🌐 Nätverksåtkomst:")
        print(f"   http://{network_ip}:{flask_port}/")
        print(f"\n💡 Dela denna URL med deltagare:")
        print(f"   http://{network_ip}:{flask_port}/")
    else:
        print(f"\n⚠️  Kunde inte hitta nätverks-IP. Kontrollera nätverksinställningar.")
    
    print(f"\n📊 Leaderboard: http://127.0.0.1:{flask_port}/leaderboard")
    print(f"{'='*60}\n")
    
    app.run(debug=True, host=flask_host, port=flask_port)

