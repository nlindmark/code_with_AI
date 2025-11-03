"""
Flask-server för leaderboard och resultathantering.
Sätter upp API-endpoints för att visa leaderboard och ta emot resultat.
"""
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from flask import Flask, jsonify, request, send_from_directory, session, redirect, url_for, render_template
import db

app = Flask(__name__)

# Läs API-nyckel från miljövariabel
API_KEY = os.getenv("API_KEY", "default_secret_key_change_me")

# Sätt session secret key
app.secret_key = os.getenv("SECRET_KEY", "change_this_secret_key_in_production")

# Competition configurations
COMPETITIONS = {
    1: {
        "name": "Code with AI - Standard",
        "description": "Standard 5-level competition",
        "levels": {
            1: {
                "title": "Nivå 1: Räkna vokaler",
                "description": "Räkna antalet vokaler (a, e, i, o, u, y, å, ä, ö) i texten: 'Programmering är roligt!'",
                "input_type": "number",
                "placeholder": "Ange antal vokaler",
                "expected_answer": "7"
            },
            2: {
                "title": "Nivå 2: Summera heltal",
                "description": "Summera alla heltal i denna text:\n\nThere are 42 apples in the basket. We found -5 rotten ones, so we removed them.\nThe remaining 37 apples are good quality.\nLater, we added 15 more apples from another batch.\nNow we have 52 total apples.\nBut wait, 8 apples were eaten, leaving us with 44.\nWe sold 12 of them for 3 dollars each, making 36 dollars profit.\nThe final count is 32 apples remaining in storage.\nEarlier today, there were -3 damaged apples that we discarded.\nTotal apples processed: 29 + 15 - 8 + 12 - 3 = 45.",
                "input_type": "number",
                "placeholder": "Ange summan",
                "expected_answer": "363"
            },
            3: {
                "title": "Nivå 3: Summa av alla värden",
                "description": "Från denna CSV:\n\nA,3\nA,4\nA,5\nB,7\nB,7\nB,8\nC,10\nC,20\nD,1\nD,2\nD,3\n\nBeräkna summan av alla värden.",
                "input_type": "number",
                "placeholder": "Ange summa av alla värden",
                "expected_answer": "70"
            },
            4: {
                "title": "Nivå 4: Caesar-chiffer",
                "description": "Dekryptera denna Caesar-chiffer (shift 7): 'Olssv, Dvysk!'",
                "input_type": "text",
                "placeholder": "Ange dekrypterad text",
                "expected_answer": "Hello, World!"
            },
            5: {
                "title": "Nivå 5: JSON-analys",
                "description": "Givet denna JSON-data:\n\n{\n  \"items\": [\n    {\"name\": \"A\", \"score\": 10},\n    {\"name\": \"B\", \"score\": 25},\n    {\"name\": \"C\", \"score\": 15}\n  ]\n}\n\nBeräkna summan av alla poäng.",
                "input_type": "number",
                "placeholder": "Ange summa av alla poäng",
                "expected_answer": "50"
            }
        }
    },
    2: {
        "name": "Code with AI - Advanced",
        "description": "Advanced 5-level competition with harder problems",
        "levels": {
            1: {
                "title": "Nivå 1: Räkna konsonanter",
                "description": "Räkna antalet konsonanter (alla bokstäver som inte är vokaler) i texten: 'Programmering är roligt!'",
                "input_type": "number",
                "placeholder": "Ange antal konsonanter",
                "expected_answer": "15"
            },
            2: {
                "title": "Nivå 2: Multiplicera heltal",
                "description": "Multiplicera alla positiva heltal i denna text:\n\nWe found 3 boxes with 4 items each.\nThen we added 2 more boxes with 5 items each.\nTotal: 3 * 4 * 2 * 5 = 120.",
                "input_type": "number",
                "placeholder": "Ange produkten",
                "expected_answer": "120"
            },
            3: {
                "title": "Nivå 3: Summa av alla värden",
                "description": "Från denna CSV:\n\nX,10\nX,20\nX,15\nY,5\nY,8\nY,12\n\nBeräkna summan av alla värden.",
                "input_type": "number",
                "placeholder": "Ange summa av alla värden",
                "expected_answer": "70"
            },
            4: {
                "title": "Nivå 4: ROT13-chiffer",
                "description": "Dekryptera denna ROT13-chiffer: 'Uryyb, Jbeyq!'",
                "input_type": "text",
                "placeholder": "Ange dekrypterad text",
                "expected_answer": "Hello, World!"
            },
            5: {
                "title": "Nivå 5: Komplex JSON-analys",
                "description": "Givet denna JSON-data:\n\n{\n  \"data\": [\n    {\"id\": 1, \"value\": 20},\n    {\"id\": 2, \"value\": 30},\n    {\"id\": 3, \"value\": 10}\n  ]\n}\n\nBeräkna summan av alla värden.",
                "input_type": "number",
                "placeholder": "Ange summan av alla värden",
                "expected_answer": "60"
            }
        }
    }
}


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
    
    if level_id < 1 or level_id > 5:
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
    
    return render_template('level.html', problem=problem, level_id=level_id, username=username)


@app.route("/submit/<int:level_id>", methods=['POST'])
def submit(level_id):
    """Hanterar svar för en nivå."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if level_id < 1 or level_id > 5:
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
                             error="Tävlingen är inte aktiv. Vänta tills tävlingen startar.")
    
    answer = request.form.get('answer', '').strip()
    if not answer:
        return render_template('level.html', 
                                 problem=problem, 
                                 level_id=level_id, 
                                 username=username,
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
                             success=True,
                             next_url=next_url,
                             next_level=next_level)
    else:
        return render_template('level.html', 
                             problem=problem, 
                             level_id=level_id, 
                             username=username,
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

