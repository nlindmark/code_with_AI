"""
Solution for Level 1: Count consonants in text.

Problem: Count the number of consonants (all letters that are NOT vowels) 
in the text: "Programmering är roligt!"
"""

def count_consonants(text: str) -> int:
    """
    Counts the number of consonants in the text.
    Consonants: All letters that are NOT vowels.
    Vowels: a, e, i, o, u, y, å, ä, ö
    
    Args:
        text: The text string to analyze
        
    Returns:
        Number of consonants in the text
    """
    # Define all vowels (Swedish + English)
    vowels = "aeiouyåäö"
    vowels += vowels.upper()
    
    count = 0
    for char in text:
        # Check if it's a letter and NOT a vowel
        if char.isalpha() and char not in vowels:
            count += 1
    
    return count


if __name__ == "__main__":
    text = "Programmering är roligt!"
    result = count_consonants(text)
    print(result)

