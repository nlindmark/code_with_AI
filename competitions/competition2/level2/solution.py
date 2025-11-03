"""
Solution for Level 2: Multiply all positive integers in a text file.

Problem: Multiply all positive integers in the input.txt file.
Note: Only multiply positive integers, ignore negative ones.
"""

import re
from pathlib import Path


def multiply_positive_integers(file_path: str) -> int:
    """
    Reads a file and multiplies all positive integers found in the text.
    Negative integers are ignored.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Product of all positive integers in the file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all integers (positive and negative) using regex
    numbers = re.findall(r'-?\d+', content)
    
    # Filter to only positive integers and convert to int
    positive_numbers = [int(num) for num in numbers if int(num) > 0]
    
    # Multiply all positive numbers
    product = 1
    for num in positive_numbers:
        product *= num
    
    return product


if __name__ == "__main__":
    # Get the path to input.txt in the same directory as this script
    script_dir = Path(__file__).parent
    input_file = script_dir / "input.txt"
    
    result = multiply_positive_integers(str(input_file))
    print(result)

