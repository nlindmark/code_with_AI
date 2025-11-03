"""
Databaslager för att lagra tävlingsresultat.
Använder SQLite3 för att spara bästa tid per nivå för varje användare.
"""
import sqlite3
import os
from typing import List, Dict, Any, Optional


DB_PATH = "competition.db"


def init_db():
    """Skapar databastabellerna om de inte redan finns."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Skapa tabell för tävlingar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        )
    """)
    
    # Skapa tabell för resultat: användare, tävling, nivå, bästa tid (ms), tidsstämpel
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            user TEXT NOT NULL,
            competition_id INT NOT NULL,
            level INT NOT NULL,
            best_ms INT NOT NULL,
            ts INT NOT NULL,
            PRIMARY KEY (user, competition_id, level)
        )
    """)
    
    # Skapa tabell för tävlingsstatus
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competition_state (
            competition_id INT PRIMARY KEY,
            is_active BOOLEAN DEFAULT FALSE,
            start_time INT DEFAULT 0
        )
    """)
    
    # Skapa tabell för alla inlämningar (för ranking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            competition_id INT NOT NULL,
            level INT NOT NULL,
            ms INT NOT NULL,
            timestamp INT NOT NULL,
            is_correct BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Migration: Lägg till competition_id kolumner om de saknas
    try:
        cursor.execute("ALTER TABLE results ADD COLUMN competition_id INT DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # Kolumnen finns redan
    
    try:
        cursor.execute("ALTER TABLE submissions ADD COLUMN competition_id INT DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # Kolumnen finns redan
    
    # Migration: Uppdatera competition_state om den har gammal struktur
    cursor.execute("PRAGMA table_info(competition_state)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'id' in columns and 'competition_id' not in columns:
        # Migrera från gammal struktur
        cursor.execute("DROP TABLE IF EXISTS competition_state_old")
        cursor.execute("ALTER TABLE competition_state RENAME TO competition_state_old")
        cursor.execute("""
            CREATE TABLE competition_state (
                competition_id INT PRIMARY KEY,
                is_active BOOLEAN DEFAULT FALSE,
                start_time INT DEFAULT 0
            )
        """)
        cursor.execute("""
            INSERT INTO competition_state (competition_id, is_active, start_time)
            SELECT 1, is_active, start_time FROM competition_state_old WHERE id = 1
        """)
        cursor.execute("DROP TABLE competition_state_old")
    
    # Sätt initial tävlingsstatus om den inte finns
    cursor.execute("SELECT COUNT(*) FROM competition_state WHERE competition_id = 1")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO competition_state (competition_id, is_active, start_time) VALUES (1, FALSE, 0)")
    
    conn.commit()
    conn.close()


def init_competitions(competitions_config: Dict[int, Dict[str, Any]]):
    """Initierar tävlingar i databasen från konfiguration."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for comp_id, comp_data in competitions_config.items():
        # Kontrollera om tävlingen redan finns
        cursor.execute("SELECT id FROM competitions WHERE id = ?", (comp_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Uppdatera befintlig
            cursor.execute(
                "UPDATE competitions SET name = ?, description = ? WHERE id = ?",
                (comp_data["name"], comp_data.get("description", ""), comp_id)
            )
        else:
            # Skapa ny
            cursor.execute(
                "INSERT INTO competitions (id, name, description) VALUES (?, ?, ?)",
                (comp_id, comp_data["name"], comp_data.get("description", ""))
            )
    
    conn.commit()
    conn.close()


def get_active_competition_id() -> int:
    """Hämtar ID för den valda tävlingen (startad eller ej)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Först försök hitta en startad tävling (is_active = TRUE)
    cursor.execute("SELECT competition_id FROM competition_state WHERE is_active = TRUE LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        conn.close()
        return row[0]
    
    # Om ingen är startad, hitta den senast skapade/uppdaterade tävlingen (den valda)
    # Använd den högsta competition_id som finns i tabellen
    cursor.execute("SELECT competition_id FROM competition_state ORDER BY competition_id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row[0]
    
    return 1  # Default till tävling 1 om ingen finns


def get_all_competitions() -> List[Dict[str, Any]]:
    """Hämtar alla tillgängliga tävlingar."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, description FROM competitions ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    
    return [{"id": row[0], "name": row[1], "description": row[2]} for row in rows]


def save_result(user: str, competition_id: int, level: int, ms: int) -> bool:
    """
    Sparar eller uppdaterar resultat om den nya tiden är bättre.
    Returnerar True om tiden förbättrades eller var första försöket.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Hämta nuvarande bästa tid om den finns
    cursor.execute(
        "SELECT best_ms, ts FROM results WHERE user = ? AND competition_id = ? AND level = ?",
        (user, competition_id, level)
    )
    existing = cursor.fetchone()
    
    import time
    current_ts = int(time.time())
    
    if existing is None:
        # Första försöket - spara direkt
        cursor.execute(
            "INSERT INTO results (user, competition_id, level, best_ms, ts) VALUES (?, ?, ?, ?, ?)",
            (user, competition_id, level, ms, current_ts)
        )
        improved = True
    elif ms < existing[0]:
        # Ny bättre tid - uppdatera
        cursor.execute(
            "UPDATE results SET best_ms = ?, ts = ? WHERE user = ? AND competition_id = ? AND level = ?",
            (ms, existing[1], user, competition_id, level)  # Behåll original tidsstämpel vid förbättring
        )
        improved = True
    else:
        improved = False
    
    conn.commit()
    conn.close()
    return improved


def load_leaderboard(competition_id: int = None) -> List[Dict[str, Any]]:
    """
    Läser in alla resultat och bygger leaderboard-strukturen.
    Sorterar efter: högsta nivå → lägsta totaltid → tidigaste tidsstämpel.
    Tid visar nu tid från tävlingsstart till inlämning istället för exekveringstid.
    """
    if competition_id is None:
        competition_id = get_active_competition_id()
    
    if competition_id is None:
        return []
    
    # Hämta tävlingsstatus för att få start_time
    competition_state = get_competition_state(competition_id)
    start_time = int(competition_state.get("start_time", 0))
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Hämta alla resultat för denna tävling
    cursor.execute(
        "SELECT user, level, best_ms, ts FROM results WHERE competition_id = ? ORDER BY user, level",
        (competition_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    # Om start_time är 0 men det finns resultat, använd det tidigaste ts som global start_time
    # Detta ger oss en baseline för alla användare, men Level 1 kan fortfarande vara > 0
    # om användaren inte var först med att lämna in Level 1
    if start_time == 0 and rows:
        all_timestamps = [row[3] for row in rows if row[3] > 0]
        if all_timestamps:
            # Använd det tidigaste ts minus 1 sekund som start_time för att säkerställa
            # att även den första inlämningen får en tid > 0 om det gick tid
            start_time = min(all_timestamps) - 1
    
    # Gruppera per användare
    user_data: Dict[str, Dict[str, Any]] = {}
    
    for user, level, best_ms, ts in rows:
        if user not in user_data:
            user_data[user] = {
                "user": user,
                "levels": {},
                "total_ms": 0,
                "max_level": 0
            }
        
        # Beräkna tid från tävlingsstart till inlämning (i millisekunder)
        if start_time > 0 and ts >= start_time:
            time_from_start_ms = (ts - start_time) * 1000
        elif start_time > 0 and ts < start_time:
            # Resultat från före tävlingsstart - borde inte hända, men hantera det
            time_from_start_ms = 0
        else:
            # Om tävlingen inte startat, använd 0
            time_from_start_ms = 0
        
        user_data[user]["levels"][str(level)] = {
            "ms": time_from_start_ms,
            "ts": ts
        }
        user_data[user]["total_ms"] += time_from_start_ms
        user_data[user]["max_level"] = max(user_data[user]["max_level"], level)
    
    # Konvertera till lista och sortera
    leaderboard = list(user_data.values())
    
    # Sortering: max_level (desc) → total_ms (asc) → tidigaste ts (asc)
    leaderboard.sort(key=lambda x: (
        -x["max_level"],  # Negativt för att sortera descending
        x["total_ms"],
        min(ts["ts"] for ts in x["levels"].values()) if x["levels"] else float('inf')
    ))
    
    return leaderboard


def get_competition_state(competition_id: int = None) -> Dict[str, Any]:
    """Hämtar tävlingsstatus för en specifik tävling eller aktiv tävling."""
    if competition_id is None:
        competition_id = get_active_competition_id()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT is_active, start_time FROM competition_state WHERE competition_id = ?",
        (competition_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        start_time = row[1] if row[1] is not None else 0
        return {"competition_id": competition_id, "is_active": bool(row[0]), "start_time": int(start_time)}
    return {"competition_id": competition_id, "is_active": False, "start_time": 0}


def set_competition_state(competition_id: int, is_active: bool, start_time: int = 0):
    """
    Sätter tävlingsstatus för en specifik tävling.
    Om start_time är 0 och raden redan finns, behåller vi det befintliga start_time.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Om tävlingen ska aktiveras, deaktivera alla andra först
    if is_active:
        cursor.execute("UPDATE competition_state SET is_active = FALSE")
    
    # Kontrollera om raden redan finns och hämta befintligt start_time
    cursor.execute("SELECT start_time FROM competition_state WHERE competition_id = ?", (competition_id,))
    existing = cursor.fetchone()
    
    if existing:
        # Uppdatera befintlig
        # Om start_time är 0 men det finns ett befintligt värde, behåll det befintliga
        if start_time == 0 and existing[0] is not None and existing[0] > 0:
            actual_start_time = existing[0]
        else:
            actual_start_time = start_time if start_time > 0 else 0
        
        cursor.execute(
            "UPDATE competition_state SET is_active = ?, start_time = ? WHERE competition_id = ?",
            (is_active, actual_start_time, competition_id)
        )
    else:
        # Skapa ny
        cursor.execute(
            "INSERT INTO competition_state (competition_id, is_active, start_time) VALUES (?, ?, ?)",
            (competition_id, is_active, start_time)
        )
    
    conn.commit()
    conn.close()


def set_active_competition(competition_id: int):
    """Sätter en tävling som vald (men startar den inte)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Deaktivera alla tävlingar (sätt is_active = FALSE)
    cursor.execute("UPDATE competition_state SET is_active = FALSE")
    
    # Kontrollera om raden redan finns
    cursor.execute("SELECT start_time, is_active FROM competition_state WHERE competition_id = ?", (competition_id,))
    existing = cursor.fetchone()
    
    if existing:
        # Uppdatera befintlig - behåll start_time och is_active från tidigare
        # Men sätt is_active = FALSE eftersom vi bara väljer, inte startar
        cursor.execute(
            "UPDATE competition_state SET is_active = FALSE WHERE competition_id = ?",
            (competition_id,)
        )
    else:
        # Skapa ny med is_active = FALSE (ej startad än)
        cursor.execute(
            "INSERT INTO competition_state (competition_id, is_active, start_time) VALUES (?, FALSE, 0)",
            (competition_id,)
        )
    
    conn.commit()
    conn.close()


def has_completed_level(user: str, competition_id: int, level: int) -> bool:
    """Kontrollerar om en användare har slutfört en specifik nivå i en tävling."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT COUNT(*) FROM results WHERE user = ? AND competition_id = ? AND level = ?",
        (user, competition_id, level)
    )
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0


def submit_answer(user: str, competition_id: int, level: int, answer: str, expected_answer: str) -> bool:
    """
    Validerar svar för en nivå och sparar om korrekt.
    Returnerar True om svaret var korrekt.
    
    expected_answer ska skickas in från competitions config.
    """
    # Jämför svar (case-insensitive för text-svar)
    if level in [1, 2, 3, 5]:  # Numeriska svar - exakt matchning
        is_correct = answer.strip() == expected_answer
    else:  # Text-svar - case-insensitive
        is_correct = answer.strip().lower() == expected_answer.lower()
    
    if is_correct:
        # Spara som korrekt resultat
        import time
        current_time = int(time.time())
        
        # Uppdatera results-tabellen
        save_result(user, competition_id, level, 0)  # 0 ms för webb-baserade svar
        
        # Lägg till i submissions-tabellen
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO submissions (user, competition_id, level, ms, timestamp, is_correct) VALUES (?, ?, ?, ?, ?, ?)",
            (user, competition_id, level, 0, current_time, True)
        )
        conn.commit()
        conn.close()
    
    return is_correct

