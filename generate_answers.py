"""
Answer generator tool for VBG CAN Bus Competition.
Analyzes the CAN log and updates expected_answer in all level config.json files.
"""
import json
import sys
from pathlib import Path

# Add competition3 directory to path to import can_parser
competition3_dir = Path(__file__).parent / "competitions" / "competition3"
sys.path.insert(0, str(competition3_dir))
from can_parser import (
    parse_busmaster_log,
    count_unique_can_ids,
    find_first_message_with_multi_byte_pattern,
    extract_timestamp_hhmmss,
    find_first_uds_message
)


def update_level1_config(log_file: str, config_path: Path):
    """Update Level 1 expected answer (unique CAN ID count)."""
    messages = parse_busmaster_log(log_file)
    unique_count = count_unique_can_ids(messages)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    config['expected_answer'] = str(unique_count)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Level 1: Updated expected answer to {unique_count}")


def update_level2_config(log_file: str, config_path: Path):
    """Update Level 2 expected answer (timestamp of first 7F 18 pattern)."""
    messages = parse_busmaster_log(log_file)
    
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
        timestamp = extract_timestamp_hhmmss(matching_msg.timestamp)
    else:
        timestamp = "NOT_FOUND"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    config['expected_answer'] = timestamp
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Level 2: Updated expected answer to {timestamp}")


def update_level3_config(log_file: str, config_path: Path):
    """Update Level 3 expected answer (timestamp of first UDS message)."""
    messages = parse_busmaster_log(log_file)
    
    first_uds = find_first_uds_message(messages)
    
    if first_uds:
        timestamp = extract_timestamp_hhmmss(first_uds.timestamp)
    else:
        timestamp = "NOT_FOUND"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    config['expected_answer'] = timestamp
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Level 3: Updated expected answer to {timestamp}")


def main():
    """Main function to generate answers for all levels."""
    base_dir = Path(__file__).parent
    competition_dir = base_dir / "competitions" / "competition3"
    log_file = base_dir / "VBG_CAN_Log.log"
    
    if not log_file.exists():
        print(f"Error: CAN log file not found at {log_file}")
        sys.exit(1)
    
    log_path = str(log_file)
    
    # Update each level
    level1_config = competition_dir / "level1" / "config.json"
    if level1_config.exists():
        update_level1_config(log_path, level1_config)
    else:
        print(f"Warning: Level 1 config not found at {level1_config}")
    
    level2_config = competition_dir / "level2" / "config.json"
    if level2_config.exists():
        update_level2_config(log_path, level2_config)
    else:
        print(f"Warning: Level 2 config not found at {level2_config}")
    
    level3_config = competition_dir / "level3" / "config.json"
    if level3_config.exists():
        update_level3_config(log_path, level3_config)
    else:
        print(f"Warning: Level 3 config not found at {level3_config}")
    
    print("\n✓ All expected answers updated!")


if __name__ == "__main__":
    main()

