"""
Solution for Level 2: Sum all integers in a text file.

Problem: Sum all integers (both positive and negative) in the input.txt file.
"""

import re
from pathlib import Path


def sum_integers_in_file(file_path: str) -> int:
    """
    Reads a file and sums all integers (both positive and negative) found in the text.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Sum of all integers in the file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all integers (positive and negative) using regex
    # Pattern: (-?\d+) matches optional minus sign followed by one or more digits
    numbers = re.findall(r'-?\d+', content)
    
    # Convert to int and sum
    total = sum(int(num) for num in numbers)
    
    return total


if __name__ == "__main__":
    # Get the path to input.txt in the same directory as this script
    script_dir = Path(__file__).parent
    input_file = script_dir / "input.txt"
    
    result = sum_integers_in_file(str(input_file))
    print(result)

