"""
Solution for Level 3: Sum all values from a CSV file.

Problem: From the data.csv file, calculate the sum of all values.
CSV format: category, value
"""

import csv
from pathlib import Path


def sum_csv_values(file_path: str) -> float:
    """
    Reads a CSV file and sums all values in the second column.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Sum of all values in the CSV
    """
    total = 0.0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                try:
                    value = float(row[1].strip())
                    total += value
                except ValueError:
                    # Skip invalid rows
                    continue
    
    return total


if __name__ == "__main__":
    # Get the path to data.csv in the same directory as this script
    script_dir = Path(__file__).parent
    csv_file = script_dir / "data.csv"
    
    result = sum_csv_values(str(csv_file))
    print(int(result))  # Print as integer since expected answer is 70

