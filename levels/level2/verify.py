"""
Verifieringsskript för nivå 2.
Kontrollerar att sum_numbers_in_file ger rätt svar och skickar resultatet.
"""
import os
import sys
from pathlib import Path

# Lägg till roten för att kunna importera common.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common import time_exec, submit_result
from solution import sum_numbers_in_file


if __name__ == "__main__":
    # Läs miljövariabler
    user = os.getenv("AI_CODE_USER", "anonymous")
    update_url = os.getenv("UPDATE_URL", "http://127.0.0.1:5000/update")
    api_key = os.getenv("API_KEY", "default_secret_key_change_me")
    
    # Beräknad korrekt summa från input.txt
    # 42 + (-5) + 37 + 15 + 52 + (-8) + 44 + 12 + 3 + 36 + 32 + (-3) + 29 + 15 + (-8) + 12 + (-3) + 45
    # = 42 - 5 + 37 + 15 + 52 - 8 + 44 + 12 + 3 + 36 + 32 - 3 + 29 + 15 - 8 + 12 - 3 + 45
    EXPECTED_SUM = 363
    
    # Hitta input.txt-filen
    input_file = Path(__file__).parent / "input.txt"
    
    print(f"📂 Läser fil: {input_file}")
    
    # Kör lösningen och mät tid
    result, elapsed_ms = time_exec(lambda: sum_numbers_in_file(str(input_file)))
    
    # Verifiera resultat
    if result != EXPECTED_SUM:
        print(f"❌ Felaktigt svar! Fick {result}, förväntades {EXPECTED_SUM}")
        sys.exit(1)
    
    print(f"✅ Nivå 2 klar! Summa: {result}, Tid: {elapsed_ms} ms")
    
    # Skicka resultat till servern
    print(f"📤 Skickar resultat för användare '{user}'...")
    submit_result(user, 2, elapsed_ms, update_url, api_key)

