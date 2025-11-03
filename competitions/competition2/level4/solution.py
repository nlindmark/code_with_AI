"""
Solution for Level 4: Decrypt ROT13 cipher.

Problem: Decrypt the ROT13 cipher from secret.txt file.
ROT13 is a special case of Caesar cipher where shift = 13.
Since alphabet has 26 letters, ROT13 encryption and decryption are the same operation.
"""

import string
from pathlib import Path


def rot13_decrypt(encrypted_text: str) -> str:
    """
    Decrypts text encrypted with ROT13 cipher.
    ROT13 is a Caesar cipher with shift 13, and since 13*2=26,
    encrypting twice gives the original, so encrypt = decrypt for ROT13.
    
    Args:
        encrypted_text: The encrypted text
        
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
            
            # ROT13: shift by 13 positions (encrypt and decrypt are same)
            new_pos = (pos + 13) % len(alphabet)
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
    
    result = rot13_decrypt(encrypted)
    print(result)

