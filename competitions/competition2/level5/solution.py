"""
Solution for Level 5: Sum all values from JSON data.

Problem: Given the JSON data in api_stub.json, calculate the sum of all values.
JSON format: {"data": [{"id": ..., "value": ...}, ...]}
"""

import json
from pathlib import Path


def sum_json_values(file_path: str) -> int:
    """
    Reads a JSON file and sums all value fields from the data array.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Sum of all values
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = 0
    
    # Extract data array
    data_array = data.get("data", [])
    
    # Sum all values
    for item in data_array:
        value = item.get("value", 0)
        total += value
    
    return total


if __name__ == "__main__":
    # Get the path to api_stub.json in the same directory as this script
    script_dir = Path(__file__).parent
    json_file = script_dir / "api_stub.json"
    
    result = sum_json_values(str(json_file))
    print(result)

