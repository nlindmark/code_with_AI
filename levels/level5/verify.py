"""
Verifieringsskript för nivå 5.
Kontrollerar att build_report genererar korrekt markdown och skickar resultatet.
"""
import os
import sys
from pathlib import Path

# Lägg till roten för att kunna importera common.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common import time_exec, submit_result
from solution import build_report


if __name__ == "__main__":
    # Läs miljövariabler
    user = os.getenv("AI_CODE_USER", "anonymous")
    update_url = os.getenv("UPDATE_URL", "http://127.0.0.1:5000/update")
    api_key = os.getenv("API_KEY", "default_secret_key_change_me")
    
    # Förväntat resultat från api_stub.json och template.md:
    # Genomsnitt: (10 + 25 + 15) / 3 = 16.666...
    # Top performer: B med score 25
    EXPECTED = """# Report

Average score: 16.666666666666668

Top performer: B (25)

"""
    
    # Hitta filerna
    api_file = Path(__file__).parent / "api_stub.json"
    template_file = Path(__file__).parent / "template.md"
    
    print(f"📂 Läser JSON: {api_file}")
    print(f"📂 Läser mall: {template_file}")
    
    # Kör lösningen och mät tid
    result, elapsed_ms = time_exec(
        lambda: build_report(str(api_file), str(template_file))
    )
    
    # Verifiera resultat (tolerans för flyttal i genomsnitt)
    # Kontrollera att strukturen är rätt
    if "# Report" not in result:
        print("❌ Saknar '# Report' i resultatet")
        sys.exit(1)
    
    if "Average score:" not in result:
        print("❌ Saknar 'Average score:' i resultatet")
        sys.exit(1)
    
    if "Top performer: B (25)" not in result:
        print(f"❌ Felaktig top performer eller poäng. Fick: {result}")
        sys.exit(1)
    
    # Kontrollera att genomsnitt är ungefär rätt (16.66...)
    lines = result.split("\n")
    avg_line = [l for l in lines if "Average score:" in l]
    if avg_line:
        avg_str = avg_line[0].split(":")[1].strip()
        avg_val = float(avg_str)
        if abs(avg_val - 16.666666666666668) > 0.1:
            print(f"❌ Felaktigt genomsnitt: {avg_val}, förväntades ~16.67")
            sys.exit(1)
    
    print(f"✅ Nivå 5 klar! Genererad rapport:\n{result}")
    print(f"⏱️  Tid: {elapsed_ms} ms")
    
    # Skicka resultat till servern
    print(f"📤 Skickar resultat för användare '{user}'...")
    submit_result(user, 5, elapsed_ms, update_url, api_key)












