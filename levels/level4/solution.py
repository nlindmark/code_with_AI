"""
Nivå 4: Caesar-chiffer-dekryptering.
Texten är krypterad med Caesar-chiffer med shift 7.
Du behöver dekryptera genom att flytta varje bokstav 7 steg bakåt i alfabetet.
"""
import string


def caesar_decrypt(path: str, shift: int = 7) -> str:
    """
    Läser en krypterad fil och dekrypterar texten med Caesar-chiffer.
    Flyttar varje bokstav 'shift' steg bakåt i alfabetet.
    
    Args:
        path: Sökväg till den krypterade filen
        shift: Antal steg att flytta bakåt (standard: 7)
        
    Returns:
        Den dekrypterade textsträngen
    """
    with open(path, 'r', encoding='utf-8') as f:
        encrypted = f.read()
    
    decrypted = []
    
    for char in encrypted:
        if char.isalpha():
            # Hämta rätt alfabet (stora eller små bokstäver)
            if char.isupper():
                alphabet = string.ascii_uppercase
            else:
                alphabet = string.ascii_lowercase
            
            # Hitta positionen i alfabetet
            pos = alphabet.index(char)
            
            # Flytta bakåt (dekryptera)
            new_pos = (pos - shift) % len(alphabet)
            decrypted.append(alphabet[new_pos])
        else:
            # Behåll icke-bokstavstecken som de är
            decrypted.append(char)
    
    return ''.join(decrypted)












