"""
Flask-server för leaderboard och resultathantering.
Sätter upp API-endpoints för att visa leaderboard och ta emot resultat.
"""
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from flask import Flask, jsonify, request, send_from_directory, session, redirect, url_for, render_template
import db
import competition_loader

app = Flask(__name__)

# Läs API-nyckel från miljövariabel
API_KEY = os.getenv("API_KEY", "default_secret_key_change_me")

# Sätt session secret key
app.secret_key = os.getenv("SECRET_KEY", "change_this_secret_key_in_production")

# Load competitions dynamically from folder structure
COMPETITIONS = competition_loader.load_competitions()


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
            return redirect(url_for('level', level_id=1))
        else:
            return render_template('login.html', error="Användarnamn måste vara alfanumeriskt och inte tomt")
    
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
    if competition_id not in COMPETITIONS:
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
    if competition_id not in COMPETITIONS:
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
                             error="Tävlingen är inte aktiv. Vänta tills tävlingen startar.")
    
    answer = request.form.get('answer', '').strip()
    if not answer:
        return render_template('level.html', 
                                 problem=problem, 
                                 level_id=level_id, 
                                 username=username,
                                 competition_id=competition_id,
                                 error="Svar krävs")
    
    # Validera svar med expected_answer från competition config
    expected_answer = problem.get("expected_answer", "")
    is_correct = db.submit_answer(username, competition_id, level_id, answer, expected_answer)
    
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
                             error="Felaktigt svar! Försök igen.")


@app.route("/leaderboard")
def leaderboard():
    """Visar leaderboard."""
    leaderboard_data = db.load_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard_data)


@app.route("/api/leaderboard")
def api_leaderboard():
    """Returnerar leaderboard som JSON."""
    leaderboard_data = db.load_leaderboard()
    return jsonify(leaderboard_data)


@app.route("/download/<int:competition_id>/<int:level_id>/<filename>")
def download_input_file(competition_id, level_id, filename):
    """
    Laddar ner input-fil för en nivå.
    Säkerhet: Validerar att tävlingen och nivån finns, och att filnamnet matchar.
    """
    # Kontrollera att tävlingen finns
    if competition_id not in COMPETITIONS:
        return "Tävling finns inte", 404
    
    competition = COMPETITIONS[competition_id]
    
    # Kontrollera att nivån finns i tävlingen
    if level_id not in competition["levels"]:
        return "Nivå finns inte", 404
    
    level = competition["levels"][level_id]
    
    # Kontrollera att nivån har en input_file och att filnamnet matchar
    if "input_file" not in level:
        return "Ingen input-fil för denna nivå", 404
    
    if level["input_file"] != filename:
        return "Ogiltigt filnamn", 403
    
    # Säkerhetskontroll: Filnamnet ska inte innehålla path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return "Ogiltigt filnamn", 403
    
    # Konstruera sökväg till filen
    from pathlib import Path
    competitions_dir = Path("competitions")
    file_path = competitions_dir / f"competition{competition_id}" / f"level{level_id}" / filename
    
    # Ytterligare säkerhetskontroll: Verifiera att filen verkligen finns på rätt plats
    if not file_path.exists() or not file_path.is_file():
        return "Fil hittades inte", 404
    
    # Verifiera att filen är inom competitions-katalogen (prevent path traversal)
    try:
        file_path.resolve().relative_to(Path("competitions").resolve())
    except ValueError:
        return "Ogiltig fil-sökväg", 403
    
    # Servera filen
    directory = str(file_path.parent)
    return send_from_directory(directory, filename, as_attachment=True)


@app.route("/solution/<int:competition_id>/<int:level_id>")
def get_solution(competition_id, level_id):
    """
    Hämtar lösningsprogrammet för en nivå.
    Returnerar solution.py innehållet som text.
    Säkerhet: Validerar att tävlingen och nivån finns.
    """
    # Kontrollera att tävlingen finns
    if competition_id not in COMPETITIONS:
        return "Tävling finns inte", 404
    
    competition = COMPETITIONS[competition_id]
    
    # Kontrollera att nivån finns i tävlingen
    if level_id not in competition["levels"]:
        return "Nivå finns inte", 404
    
    level = competition["levels"][level_id]
    
    # Kontrollera att nivån har en solution file
    if "solution_file" not in level:
        return "Ingen lösning finns för denna nivå", 404
    
    # Konstruera sökväg till solution.py
    from pathlib import Path
    competitions_dir = Path("competitions")
    solution_path = competitions_dir / f"competition{competition_id}" / f"level{level_id}" / "solution.py"
    
    # Säkerhetskontroll: Verifiera att filen verkligen finns på rätt plats
    if not solution_path.exists() or not solution_path.is_file():
        return "Lösningsfil hittades inte", 404
    
    # Verifiera att filen är inom competitions-katalogen (prevent path traversal)
    try:
        solution_path.resolve().relative_to(Path("competitions").resolve())
    except ValueError:
        return "Ogiltig fil-sökväg", 403
    
    # Läs och returnera filinnehållet
    try:
        with open(solution_path, 'r', encoding='utf-8') as f:
            solution_content = f.read()
        return solution_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return f"Fel vid läsning av lösningsfil: {e}", 500


@app.route("/admin")
def admin():
    """Admin-kontrollpanel för tävlingsledare."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return "API-nyckel krävs", 403
    
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
        return jsonify({"error": "Ogiltig API-nyckel"}), 403
    
    competition_id = db.get_active_competition_id()
    import time
    start_time = int(time.time())
    db.set_competition_state(competition_id, True, start_time)
    
    return jsonify({"success": True, "message": "Tävling startad!"})


@app.route("/admin/stop", methods=["POST"])
def admin_stop():
    """Stoppar den aktiva tävlingen."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return jsonify({"error": "Ogiltig API-nyckel"}), 403
    
    competition_id = db.get_active_competition_id()
    # Behåll start_time när vi stoppar - sätt bara is_active till False
    current_state = db.get_competition_state(competition_id)
    existing_start_time = current_state.get("start_time", 0)
    db.set_competition_state(competition_id, False, existing_start_time)
    
    return jsonify({"success": True, "message": "Tävling stoppad!"})


@app.route("/admin/competitions", methods=["POST"])
def admin_set_active_competition():
    """Sätter aktiv tävling."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return jsonify({"error": "Ogiltig API-nyckel"}), 403
    
    data = request.json
    if not data or "competition_id" not in data:
        return jsonify({"error": "Saknar competition_id"}), 400
    
    competition_id = data["competition_id"]
    
    # Kontrollera att tävlingen finns
    if competition_id not in COMPETITIONS:
        return jsonify({"error": "Ogiltig tävling"}), 400
    
    # Sätt som aktiv
    db.set_active_competition(competition_id)
    
    return jsonify({"success": True, "message": f"Tävling {competition_id} är nu aktiv"})


@app.route("/update", methods=["POST"])
def update():
    """
    Tar emot resultat från användare och sparar om det är bättre.
    Förväntar JSON: {"user": str, "level": int, "ms": int}
    """
    data = request.json
    
    if not data or "user" not in data or "level" not in data or "ms" not in data:
        return jsonify({"error": "Saknar user, level eller ms"}), 400
    
    user = data["user"]
    level = data["level"]
    ms = data["ms"]
    
    # Validera att nivå och tid är positiva
    if not isinstance(level, int) or level < 1:
        return jsonify({"error": "Ogiltig nivå"}), 400
    
    if not isinstance(ms, int) or ms < 0:
        return jsonify({"error": "Ogiltig tid"}), 400
    
    competition_id = db.get_active_competition_id()
    
    # Kontrollera att tävlingen är aktiv
    competition_state = db.get_competition_state(competition_id)
    if not competition_state.get("is_active", False):
        return jsonify({"error": "Tävlingen är inte aktiv"}), 403
    
    # Kontrollera att nivån finns i tävlingen
    if competition_id not in COMPETITIONS:
        return jsonify({"error": "Tävlingen finns inte"}), 400
    
    if level not in COMPETITIONS[competition_id]["levels"]:
        return jsonify({"error": "Nivån finns inte i tävlingen"}), 400
    
    improved = db.save_result(user, competition_id, level, ms)
    
    return jsonify({
        "success": True,
        "improved": improved,
        "message": "Tid förbättrad!" if improved else "Ingen förbättring"
    })


@app.route("/reset", methods=["GET"])
def reset():
    """
    Raderar alla resultat. Kräver X-API-Key header.
    """
    api_key_header = request.headers.get("X-API-Key")
    
    if api_key_header != API_KEY:
        return jsonify({"error": "Ogiltig API-nyckel"}), 403
    
    # Radera databasfilen och skapa ny tabell
    import sqlite3
    import os as os_module
    
    if os_module.path.exists(db.DB_PATH):
        os_module.remove(db.DB_PATH)
    
    db.init_db()
    db.init_competitions(COMPETITIONS)
    
    return jsonify({"success": True, "message": "Alla resultat raderade"})


if __name__ == "__main__":
    # Initiera databas vid start
    db.init_db()
    
    # Initiera tävlingar i databasen
    db.init_competitions(COMPETITIONS)
    
    # Starta Flask-server
    print(f"🚀 Server startar på http://127.0.0.1:5000/")
    print(f"📊 Leaderboard: http://127.0.0.1:5000/leaderboard")
    app.run(debug=True, host="127.0.0.1", port=5000)

