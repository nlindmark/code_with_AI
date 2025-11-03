"""
Solution for Level 4: Decrypt Caesar cipher.

Problem: Decrypt the Caesar cipher (shift 7) from secret.txt file.
Shift 7 means each letter was shifted forward by 7 positions, 
so we decrypt by shifting backward by 7 positions.
"""

import string
from pathlib import Path


def caesar_decrypt(encrypted_text: str, shift: int = 7) -> str:
    """
    Decrypts text encrypted with Caesar cipher by shifting letters backward.
    
    Args:
        encrypted_text: The encrypted text
        shift: Number of positions to shift backward (default: 7)
        
    Returns:
        The decrypted text
    """
    decrypted = []
    
    for char in encrypted_text:
        if char.isalpha():
            # Get the appropriate alphabet (uppercase or lowercase)
            if char.isupper():
                alphabet = string.ascii_uppercase
            else:
                alphabet = string.ascii_lowercase
            
            # Find position in alphabet
            pos = alphabet.index(char)
            
            # Shift backward (decrypt)
            new_pos = (pos - shift) % len(alphabet)
            decrypted.append(alphabet[new_pos])
        else:
            # Keep non-letter characters as they are
            decrypted.append(char)
    
    return ''.join(decrypted)


if __name__ == "__main__":
    # Get the path to secret.txt in the same directory as this script
    script_dir = Path(__file__).parent
    secret_file = script_dir / "secret.txt"
    
    with open(secret_file, 'r', encoding='utf-8') as f:
        encrypted = f.read().strip()
    
    result = caesar_decrypt(encrypted, shift=7)
    print(result)

