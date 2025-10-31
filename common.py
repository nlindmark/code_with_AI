"""
Gemensamma verktyg för timing och resultatinlämning.
Används av alla verify.py-filer.
"""
import time
import os
import requests
from typing import Any, Tuple, Callable


def time_exec(func: Callable) -> Tuple[Any, int]:
    """
    Kör en funktion och mäter exekveringstid i millisekunder.
    Returnerar (resultat, förfluten_tid_ms).
    """
    start = time.perf_counter()
    result = func()
    elapsed = time.perf_counter() - start
    elapsed_ms = int(elapsed * 1000)
    return result, elapsed_ms


def submit_result(user: str, level: int, ms: int, update_url: str, api_key: str):
    """
    Skickar resultat till servern via POST-request.
    Hanterar fel gracefully - skriver varning men stoppar inte körningen.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": api_key
        }
        payload = {
            "user": user,
            "level": level,
            "ms": ms
        }
        
        response = requests.post(update_url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        
        print(f"✓ Resultat skickat till servern")
    except requests.exceptions.RequestException as e:
        print(f"⚠ Varning: Kunde inte skicka resultat till server: {e}")
        print("   Fortsätter utan att uppdatera leaderboard...")



