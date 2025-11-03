"""
Solution for Level 1: Count Unique CAN IDs
"""
import sys
from pathlib import Path

# Add competition3 directory to path to import can_parser
sys.path.insert(0, str(Path(__file__).parent.parent))
from can_parser import parse_busmaster_log, count_unique_can_ids


def solve_level1(log_file: str) -> int:
    """
    Count unique CAN IDs in the log file.
    
    Args:
        log_file: Path to CAN log file
        
    Returns:
        Number of unique CAN IDs
    """
    messages = parse_busmaster_log(log_file)
    unique_count = count_unique_can_ids(messages)
    return unique_count


if __name__ == "__main__":
    log_path = Path(__file__).parent / "VBG_CAN_Log.log"
    result = solve_level1(str(log_path))
    print(f"Number of unique CAN IDs: {result}")

