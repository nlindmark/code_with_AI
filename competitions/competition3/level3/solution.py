"""
Solution for Level 3: First UDS Diagnostic Message Detection
"""
import sys
from pathlib import Path

# Add competition3 directory to path to import can_parser
sys.path.insert(0, str(Path(__file__).parent.parent))
from can_parser import (
    parse_busmaster_log,
    find_first_uds_message,
    extract_timestamp_hhmmss
)


def solve_level3(log_file: str) -> str:
    """
    Find the first UDS diagnostic message (CAN IDs 0x7E0-0x7EF).
    
    Args:
        log_file: Path to CAN log file
        
    Returns:
        Timestamp in HH:MM:SS format
    """
    messages = parse_busmaster_log(log_file)
    
    first_uds = find_first_uds_message(messages)
    
    if first_uds:
        return extract_timestamp_hhmmss(first_uds.timestamp)
    else:
        return "NOT_FOUND"


if __name__ == "__main__":
    log_path = Path(__file__).parent / "VBG_CAN_Log.log"
    result = solve_level3(str(log_path))
    print(f"First UDS diagnostic message timestamp: {result}")

