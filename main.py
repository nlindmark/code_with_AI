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
    
    # Problembeskrivningar
    problems = {
        1: {
            "title": "Nivå 1: Räkna vokaler",
            "description": "Räkna antalet vokaler (a, e, i, o, u, y, å, ä, ö) i texten: 'Programmering är roligt!'",
            "input_type": "number",
            "placeholder": "Ange antal vokaler"
        },
        2: {
            "title": "Nivå 2: Summera heltal",
            "description": "Summera alla heltal i denna text:\n\nThere are 42 apples in the basket. We found -5 rotten ones, so we removed them.\nThe remaining 37 apples are good quality.\nLater, we added 15 more apples from another batch.\nNow we have 52 total apples.\nBut wait, 8 apples were eaten, leaving us with 44.\nWe sold 12 of them for 3 dollars each, making 36 dollars profit.\nThe final count is 32 apples remaining in storage.\nEarlier today, there were -3 damaged apples that we discarded.\nTotal apples processed: 29 + 15 - 8 + 12 - 3 = 45.",
            "input_type": "number",
            "placeholder": "Ange summan"
        },
        3: {
            "title": "Nivå 3: Genomsnitt per kategori",
            "description": "Beräkna genomsnitt per kategori från denna CSV:\n\nA,3\nA,4\nA,5\nB,7\nB,7\nB,8\nC,10\nC,20\nD,1\nD,2\nD,3\n\nSvara i format: A=4.0,B=7.33,C=15.0,D=2.0",
            "input_type": "text",
            "placeholder": "A=4.0,B=7.33,C=15.0,D=2.0"
        },
        4: {
            "title": "Nivå 4: Caesar-chiffer",
            "description": "Dekryptera denna Caesar-chiffer (shift 7): 'Olssv, Dvysk!'",
            "input_type": "text",
            "placeholder": "Ange dekrypterad text"
        },
        5: {
            "title": "Nivå 5: JSON-analys",
            "description": "Givet denna JSON-data:\n\n{\n  \"items\": [\n    {\"name\": \"A\", \"score\": 10},\n    {\"name\": \"B\", \"score\": 25},\n    {\"name\": \"C\", \"score\": 15}\n  ]\n}\n\nBeräkna genomsnittlig poäng och hitta topprestationen.\nSvara i format: avg=16.67,top=B",
            "input_type": "text",
            "placeholder": "avg=16.67,top=B"
        }
    }
    
    problem = problems.get(level_id)
    if not problem:
        return redirect(url_for('leaderboard'))
    
    return render_template('level.html', problem=problem, level_id=level_id, username=session['username'])


@app.route("/submit/<int:level_id>", methods=['POST'])
def submit(level_id):
    """Hanterar svar för en nivå."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if level_id < 1 or level_id > 5:
        return redirect(url_for('leaderboard'))
    
    answer = request.form.get('answer', '').strip()
    if not answer:
        # Hämta problembeskrivning igen
        problems = {
            1: {
                "title": "Nivå 1: Räkna vokaler",
                "description": "Räkna antalet vokaler (a, e, i, o, u, y, å, ä, ö) i texten: 'Programmering är roligt!'",
                "input_type": "number",
                "placeholder": "Ange antal vokaler"
            },
            2: {
                "title": "Nivå 2: Summera heltal",
                "description": "Summera alla heltal i denna text:\n\nThere are 42 apples in the basket. We found -5 rotten ones, so we removed them.\nThe remaining 37 apples are good quality.\nLater, we added 15 more apples from another batch.\nNow we have 52 total apples.\nBut wait, 8 apples were eaten, leaving us with 44.\nWe sold 12 of them for 3 dollars each, making 36 dollars profit.\nThe final count is 32 apples remaining in storage.\nEarlier today, there were -3 damaged apples that we discarded.\nTotal apples processed: 29 + 15 - 8 + 12 - 3 = 45.",
                "input_type": "number",
                "placeholder": "Ange summan"
            },
            3: {
                "title": "Nivå 3: Genomsnitt per kategori",
                "description": "Beräkna genomsnitt per kategori från denna CSV:\n\nA,3\nA,4\nA,5\nB,7\nB,7\nB,8\nC,10\nC,20\nD,1\nD,2\nD,3\n\nSvara i format: A=4.0,B=7.33,C=15.0,D=2.0",
                "input_type": "text",
                "placeholder": "A=4.0,B=7.33,C=15.0,D=2.0"
            },
            4: {
                "title": "Nivå 4: Caesar-chiffer",
                "description": "Dekryptera denna Caesar-chiffer (shift 7): 'Olssv, Dvysk!'",
                "input_type": "text",
                "placeholder": "Ange dekrypterad text"
            },
            5: {
                "title": "Nivå 5: JSON-analys",
                "description": "Givet denna JSON-data:\n\n{\n  \"items\": [\n    {\"name\": \"A\", \"score\": 10},\n    {\"name\": \"B\", \"score\": 25},\n    {\"name\": \"C\", \"score\": 15}\n  ]\n}\n\nBeräkna genomsnittlig poäng och hitta topprestationen.\nSvara i format: avg=16.67,top=B",
                "input_type": "text",
                "placeholder": "avg=16.67,top=B"
            }
        }
        
        return render_template('level.html', 
                                 problem=problems.get(level_id), 
                                 level_id=level_id, 
                                 username=session['username'],
                                 error="Svar krävs")
    
    # Validera svar
    is_correct = db.submit_answer(session['username'], level_id, answer)
    
    if is_correct:
        # Gå till nästa nivå eller leaderboard
        if level_id < 5:
            return redirect(url_for('level', level_id=level_id + 1))
        else:
            return redirect(url_for('leaderboard'))
    else:
        # Hämta problembeskrivning igen för felmeddelande
        problems = {
            1: {
                "title": "Nivå 1: Räkna vokaler",
                "description": "Räkna antalet vokaler (a, e, i, o, u, y, å, ä, ö) i texten: 'Programmering är roligt!'",
                "input_type": "number",
                "placeholder": "Ange antal vokaler"
            },
            2: {
                "title": "Nivå 2: Summera heltal",
                "description": "Summera alla heltal i denna text:\n\nThere are 42 apples in the basket. We found -5 rotten ones, so we removed them.\nThe remaining 37 apples are good quality.\nLater, we added 15 more apples from another batch.\nNow we have 52 total apples.\nBut wait, 8 apples were eaten, leaving us with 44.\nWe sold 12 of them for 3 dollars each, making 36 dollars profit.\nThe final count is 32 apples remaining in storage.\nEarlier today, there were -3 damaged apples that we discarded.\nTotal apples processed: 29 + 15 - 8 + 12 - 3 = 45.",
                "input_type": "number",
                "placeholder": "Ange summan"
            },
            3: {
                "title": "Nivå 3: Genomsnitt per kategori",
                "description": "Beräkna genomsnitt per kategori från denna CSV:\n\nA,3\nA,4\nA,5\nB,7\nB,7\nB,8\nC,10\nC,20\nD,1\nD,2\nD,3\n\nSvara i format: A=4.0,B=7.33,C=15.0,D=2.0",
                "input_type": "text",
                "placeholder": "A=4.0,B=7.33,C=15.0,D=2.0"
            },
            4: {
                "title": "Nivå 4: Caesar-chiffer",
                "description": "Dekryptera denna Caesar-chiffer (shift 7): 'Olssv, Dvysk!'",
                "input_type": "text",
                "placeholder": "Ange dekrypterad text"
            },
            5: {
                "title": "Nivå 5: JSON-analys",
                "description": "Givet denna JSON-data:\n\n{\n  \"items\": [\n    {\"name\": \"A\", \"score\": 10},\n    {\"name\": \"B\", \"score\": 25},\n    {\"name\": \"C\", \"score\": 15}\n  ]\n}\n\nBeräkna genomsnittlig poäng och hitta topprestationen.\nSvara i format: avg=16.67,top=B",
                "input_type": "text",
                "placeholder": "avg=16.67,top=B"
            }
        }
        
        return render_template('level.html', 
                             problem=problems.get(level_id), 
                             level_id=level_id, 
                             username=session['username'],
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
    
    competition_state = db.get_competition_state()
    return render_template('admin.html', state=competition_state)


@app.route("/admin/start", methods=["POST"])
def admin_start():
    """Startar tävlingen."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return jsonify({"error": "Ogiltig API-nyckel"}), 403
    
    import time
    start_time = int(time.time())
    db.set_competition_state(True, start_time)
    
    return jsonify({"success": True, "message": "Tävling startad!"})


@app.route("/admin/stop", methods=["POST"])
def admin_stop():
    """Stoppar tävlingen."""
    api_key_header = request.headers.get("X-API-Key")
    if api_key_header != API_KEY:
        return jsonify({"error": "Ogiltig API-nyckel"}), 403
    
    db.set_competition_state(False, 0)
    
    return jsonify({"success": True, "message": "Tävling stoppad!"})


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
    
    improved = db.save_result(user, level, ms)
    
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
    
    return jsonify({"success": True, "message": "Alla resultat raderade"})


if __name__ == "__main__":
    # Initiera databas vid start
    db.init_db()
    
    # Starta Flask-server
    print(f"🚀 Server startar på http://127.0.0.1:5000/")
    print(f"📊 Leaderboard: http://127.0.0.1:5000/leaderboard")
    app.run(debug=True, host="127.0.0.1", port=5000)

