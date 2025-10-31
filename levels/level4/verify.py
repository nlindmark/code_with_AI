"""
Verifieringsskript för nivå 4.
Kontrollerar att caesar_decrypt ger rätt dekrypterad text och skickar resultatet.
"""
import os
import sys
from pathlib import Path

# Lägg till roten för att kunna importera common.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common import time_exec, submit_result
from solution import caesar_decrypt


if __name__ == "__main__":
    # Läs miljövariabler
    user = os.getenv("AI_CODE_USER", "anonymous")
    update_url = os.getenv("UPDATE_URL", "http://127.0.0.1:5000/update")
    api_key = os.getenv("API_KEY", "default_secret_key_change_me")
    
    # Förväntad dekrypterad text: "Hello, World!"
    EXPECTED = "Hello, World!"
    
    # Hitta secret.txt-filen
    secret_file = Path(__file__).parent / "secret.txt"
    
    print(f"📂 Läser fil: {secret_file}")
    
    # Kör lösningen och mät tid
    result, elapsed_ms = time_exec(lambda: caesar_decrypt(str(secret_file), shift=7))
    
    # Ta bort eventuella radbyten
    result = result.strip()
    
    # Verifiera resultat
    if result != EXPECTED:
        print(f"❌ Felaktig dekryptering! Fick '{result}', förväntades '{EXPECTED}'")
        sys.exit(1)
    
    print(f"✅ Nivå 4 klar! Dekrypterad text: '{result}', Tid: {elapsed_ms} ms")
    
    # Skicka resultat till servern
    print(f"📤 Skickar resultat för användare '{user}'...")
    submit_result(user, 4, elapsed_ms, update_url, api_key)

