"""
Nivå 1: Räkna vokaler i text.
Skall räkna både engelska och svenska vokaler (a, e, i, o, u, y, å, ä, ö).
Skall vara skiftlägesokänslig (stora och små bokstäver räknas lika).
"""
import re


def count_vowels(text: str) -> int:
    """
    Räknar antalet vokaler i texten.
    Vokaler: a, e, i, o, u, y, å, ä, ö (både stora och små).
    
    Args:
        text: Textsträngen att analysera
        
    Returns:
        Antal vokaler i texten
    """
    # Definiera alla vokaler (svenska + engelska)
    vowels = "aeiouyåäö"
    vowels += vowels.upper()  # Lägg till stora bokstäver
    
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    
    return count



