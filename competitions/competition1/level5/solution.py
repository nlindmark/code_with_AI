"""
Solution for Level 5: Sum all scores from JSON data.

Problem: Given the JSON data in api_stub.json, calculate the sum of all scores.
JSON format: {"items": [{"name": "...", "score": ...}, ...]}
"""

import json
from pathlib import Path


def sum_json_scores(file_path: str) -> int:
    """
    Reads a JSON file and sums all score values from the items array.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Sum of all scores
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = 0
    
    # Extract items array
    items = data.get("items", [])
    
    # Sum all scores
    for item in items:
        score = item.get("score", 0)
        total += score
    
    return total


if __name__ == "__main__":
    # Get the path to api_stub.json in the same directory as this script
    script_dir = Path(__file__).parent
    json_file = script_dir / "api_stub.json"
    
    result = sum_json_scores(str(json_file))
    print(result)

