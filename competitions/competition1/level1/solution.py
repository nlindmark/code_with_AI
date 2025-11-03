"""
Solution for Level 1: Count vowels in text.

Problem: Count the number of vowels (a, e, i, o, u, y, å, ä, ö) 
in the text: "Programmering är roligt!"
"""

def count_vowels(text: str) -> int:
    """
    Counts the number of vowels in the text.
    Vowels: a, e, i, o, u, y, å, ä, ö (both uppercase and lowercase).
    
    Args:
        text: The text string to analyze
        
    Returns:
        Number of vowels in the text
    """
    # Define all vowels (Swedish + English)
    vowels = "aeiouyåäö"
    vowels += vowels.upper()  # Add uppercase letters
    
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    
    return count


if __name__ == "__main__":
    text = "Programmering är roligt!"
    result = count_vowels(text)
    print(result)

