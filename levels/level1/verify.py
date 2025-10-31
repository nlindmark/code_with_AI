"""
Verifieringsskript för nivå 1.
Kör testfall för solution.py och skickar resultatet till servern.
"""
import os
import sys
from pathlib import Path

# Lägg till roten för att kunna importera common.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common import time_exec, submit_result
from solution import count_vowels


def run_tests():
    """Kör testfall för att verifiera lösningen."""
    test_cases = [
        ("", 0),  # Tom sträng
        ("Hello", 2),  # e, o
        ("Äpple", 2),  # Ä, e
        ("Sweden", 2),  # e, e
        ("ÅåäöÖ", 5),  # Alla svenska vokaler
        ("AeIoUy", 6),  # Alla engelska vokaler + y
        ("Programmering är roligt!", 7),  # o, a, e, i, å, o, i
        ("123ABC!@#", 1),  # Endast A
    ]
    
    print("🧪 Kör testfall...")
    for i, (text, expected) in enumerate(test_cases, 1):
        result = count_vowels(text)
        if result != expected:
            print(f"❌ Test {i} misslyckades: '{text}' gav {result}, förväntades {expected}")
            return False
        else:
            print(f"✅ Test {i} passerade: '{text}' → {result} vokaler")
    
    return True


if __name__ == "__main__":
    # Läs miljövariabler
    user = os.getenv("AI_CODE_USER", "anonymous")
    update_url = os.getenv("UPDATE_URL", "http://127.0.0.1:5000/update")
    api_key = os.getenv("API_KEY", "default_secret_key_change_me")
    
    # Kör testfall
    if not run_tests():
        print("❌ Några testfall misslyckades. Fixa din lösning först!")
        sys.exit(1)
    
    # Mät exekveringstid på en större test
    print("\n⏱️  Mäter exekveringstid...")
    test_text = "Programmering är roligt! " * 1000
    result, elapsed_ms = time_exec(lambda: count_vowels(test_text))
    
    print(f"✅ Nivå 1 klar! Tid: {elapsed_ms} ms")
    
    # Skicka resultat till servern
    print(f"📤 Skickar resultat för användare '{user}'...")
    submit_result(user, 1, elapsed_ms, update_url, api_key)

