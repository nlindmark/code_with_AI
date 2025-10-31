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
    
    # Skapa tabell för resultat: användare, nivå, bästa tid (ms), tidsstämpel
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            user TEXT NOT NULL,
            level INT NOT NULL,
            best_ms INT NOT NULL,
            ts INT NOT NULL,
            PRIMARY KEY (user, level)
        )
    """)
    
    # Skapa tabell för tävlingsstatus
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competition_state (
            id INTEGER PRIMARY KEY,
            is_active BOOLEAN DEFAULT FALSE,
            start_time INT DEFAULT 0
        )
    """)
    
    # Skapa tabell för alla inlämningar (för ranking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            level INT NOT NULL,
            ms INT NOT NULL,
            timestamp INT NOT NULL,
            is_correct BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Sätt initial tävlingsstatus om den inte finns
    cursor.execute("SELECT COUNT(*) FROM competition_state")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO competition_state (is_active, start_time) VALUES (FALSE, 0)")
    
    conn.commit()
    conn.close()


def save_result(user: str, level: int, ms: int) -> bool:
    """
    Sparar eller uppdaterar resultat om den nya tiden är bättre.
    Returnerar True om tiden förbättrades eller var första försöket.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Hämta nuvarande bästa tid om den finns
    cursor.execute(
        "SELECT best_ms, ts FROM results WHERE user = ? AND level = ?",
        (user, level)
    )
    existing = cursor.fetchone()
    
    import time
    current_ts = int(time.time())
    
    if existing is None:
        # Första försöket - spara direkt
        cursor.execute(
            "INSERT INTO results (user, level, best_ms, ts) VALUES (?, ?, ?, ?)",
            (user, level, ms, current_ts)
        )
        improved = True
    elif ms < existing[0]:
        # Ny bättre tid - uppdatera
        cursor.execute(
            "UPDATE results SET best_ms = ?, ts = ? WHERE user = ? AND level = ?",
            (ms, existing[1], user, level)  # Behåll original tidsstämpel vid förbättring
        )
        improved = True
    else:
        improved = False
    
    conn.commit()
    conn.close()
    return improved


def load_leaderboard() -> List[Dict[str, Any]]:
    """
    Läser in alla resultat och bygger leaderboard-strukturen.
    Sorterar efter: högsta nivå → lägsta totaltid → tidigaste tidsstämpel.
    Tid visar nu tid från tävlingsstart till inlämning istället för exekveringstid.
    """
    # Hämta tävlingsstatus för att få start_time
    competition_state = get_competition_state()
    start_time = competition_state.get("start_time", 0)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Hämta alla resultat
    cursor.execute("SELECT user, level, best_ms, ts FROM results ORDER BY user, level")
    rows = cursor.fetchall()
    conn.close()
    
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
        if start_time > 0:
            time_from_start_ms = (ts - start_time) * 1000
        else:
            # Om tävlingen inte startat, använd 0 (skulle inte hända om tävling är aktiv)
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


def get_competition_state() -> Dict[str, Any]:
    """Hämtar aktuell tävlingsstatus."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT is_active, start_time FROM competition_state WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"is_active": bool(row[0]), "start_time": row[1]}
    return {"is_active": False, "start_time": 0}


def set_competition_state(is_active: bool, start_time: int = 0):
    """Sätter tävlingsstatus."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE competition_state SET is_active = ?, start_time = ? WHERE id = 1",
        (is_active, start_time)
    )
    conn.commit()
    conn.close()


def has_completed_level(user: str, level: int) -> bool:
    """Kontrollerar om en användare har slutfört en specifik nivå."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT COUNT(*) FROM results WHERE user = ? AND level = ?",
        (user, level)
    )
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0


def submit_answer(user: str, level: int, answer: str) -> bool:
    """
    Validerar svar för en nivå och sparar om korrekt.
    Returnerar True om svaret var korrekt.
    """
    # Hämta förväntat svar baserat på nivå
    expected_answers = {
        1: "7",  # "Programmering är roligt!" har 7 vokaler
        2: "363",  # Summan från input.txt
        3: "A=4.0,B=7.33,C=15.0,D=2.0",  # Genomsnitt per kategori
        4: "Hello, World!",  # Caesar dekryptering
        5: "avg=16.67,top=B"  # JSON + mall
    }
    
    expected = expected_answers.get(level, "")
    
    # Jämför svar (case-insensitive för vissa nivåer)
    if level in [1, 2, 3, 5]:  # Numeriska svar
        is_correct = answer.strip() == expected
    else:  # Text-svar
        is_correct = answer.strip().lower() == expected.lower()
    
    if is_correct:
        # Spara som korrekt resultat
        import time
        current_time = int(time.time())
        
        # Uppdatera results-tabellen
        save_result(user, level, 0)  # 0 ms för webb-baserade svar
        
        # Lägg till i submissions-tabellen
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO submissions (user, level, ms, timestamp, is_correct) VALUES (?, ?, ?, ?, ?)",
            (user, level, 0, current_time, True)
        )
        conn.commit()
        conn.close()
    
    return is_correct

