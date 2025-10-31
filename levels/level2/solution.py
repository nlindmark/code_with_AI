"""
Nivå 2: Summera alla heltal från en fil.
Filen innehåller blandad text med positiva och negativa heltal.
Du behöver extrahera alla heltal och summera dem.
"""
import re


def sum_numbers_in_file(path: str) -> int:
    """
    Läser en fil och summerar alla heltal (både positiva och negativa) som finns i texten.
    
    Args:
        path: Sökväg till filen som ska läsas
        
    Returns:
        Summan av alla heltal i filen
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Hitta alla heltal (positiva och negativa) med regex
    # Pattern: (-?\d+) matchar valfritt minustecken följt av en eller flera siffror
    numbers = re.findall(r'-?\d+', content)
    
    # Konvertera till int och summera
    total = sum(int(num) for num in numbers)
    
    return total

