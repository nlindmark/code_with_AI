"""
Solution for Level 2: Timestamp Pattern Detection
"""
import sys
from pathlib import Path

# Add competition3 directory to path to import can_parser
sys.path.insert(0, str(Path(__file__).parent.parent))
from can_parser import (
    parse_busmaster_log,
    find_first_message_with_multi_byte_pattern,
    extract_timestamp_hhmmss
)


def solve_level2(log_file: str) -> str:
    """
    Find first message with CAN ID 0xCF11000 where byte 0 = 0x7F and byte 1 = 0x18.
    
    Args:
        log_file: Path to CAN log file
        
    Returns:
        Timestamp in HH:MM:SS format
    """
    messages = parse_busmaster_log(log_file)
    
    # Look for pattern: byte 0 = 7F, byte 1 = 18
    pattern = {
        0: "7F",
        1: "18"
    }
    
    matching_msg = find_first_message_with_multi_byte_pattern(
        messages,
        "0xCF11000",
        pattern
    )
    
    if matching_msg:
        return extract_timestamp_hhmmss(matching_msg.timestamp)
    else:
        return "NOT_FOUND"


if __name__ == "__main__":
    log_path = Path(__file__).parent / "VBG_CAN_Log.log"
    result = solve_level2(str(log_path))
    print(f"First timestamp with pattern 7F 18 in 0xCF11000: {result}")

