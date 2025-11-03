"""
Verifieringsskript för nivå 3.
Kontrollerar att avg_per_category ger rätt genomsnitt och skickar resultatet.
"""
import os
import sys
from pathlib import Path

# Lägg till roten för att kunna importera common.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common import time_exec, submit_result
from solution import avg_per_category


if __name__ == "__main__":
    # Läs miljövariabler
    user = os.getenv("AI_CODE_USER", "anonymous")
    update_url = os.getenv("UPDATE_URL", "http://127.0.0.1:5000/update")
    api_key = os.getenv("API_KEY", "default_secret_key_change_me")
    
    # Förväntat resultat från data.csv:
    # A: (3+4+5)/3 = 4.0
    # B: (7+7+8)/3 = 7.333...
    # C: (10+20)/2 = 15.0
    # D: (1+2+3)/3 = 2.0
    EXPECTED = {
        "A": 4.0,
        "B": 7.333333333333333,  # ~7.33
        "C": 15.0,
        "D": 2.0
    }
    
    # Hitta CSV-filen
    csv_file = Path(__file__).parent / "data.csv"
    
    print(f"📂 Läser CSV-fil: {csv_file}")
    
    # Kör lösningen och mät tid
    result, elapsed_ms = time_exec(lambda: avg_per_category(str(csv_file)))
    
    # Verifiera resultat (tolerans för flyttal)
    if len(result) != len(EXPECTED):
        print(f"❌ Fel antal kategorier! Fick {len(result)}, förväntades {len(EXPECTED)}")
        sys.exit(1)
    
    for category, expected_avg in EXPECTED.items():
        if category not in result:
            print(f"❌ Saknar kategori '{category}' i resultatet")
            sys.exit(1)
        
        actual = result[category]
        # Tillåt liten avvikelse för flyttal (0.001)
        if abs(actual - expected_avg) > 0.001:
            print(f"❌ Fel genomsnitt för '{category}': fick {actual}, förväntades {expected_avg}")
            sys.exit(1)
    
    print(f"✅ Nivå 3 klar! Genomsnitt per kategori: {result}, Tid: {elapsed_ms} ms")
    
    # Skicka resultat till servern
    print(f"📤 Skickar resultat för användare '{user}'...")
    submit_result(user, 3, elapsed_ms, update_url, api_key)












