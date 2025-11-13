#!/usr/bin/env python3
"""
VBG Smart Coupling Safety Challenge - Level 1: The Incident Report
Solution: Count total CAN messages in the log file

Task: Determine how many TOTAL CAN messages were recorded during the incident.
Answer: 38407
"""

def count_can_messages(log_file):
    """
    Count the total number of CAN messages in the log file.
    
    CAN messages are lines that start with a timestamp and contain "Rx"
    followed by a channel number and CAN ID.
    
    Example of a CAN message line:
    11:38:07:5682 Rx 1 0xCF073E3 x 8 FE E3 4B 49 9A 01 00 00
    """
    count = 0
    
    with open(log_file, 'r') as f:
        for line in f:
            # Skip header lines (start with ***)
            if line.startswith('***'):
                continue
            
            # CAN messages contain "Rx" followed by channel and CAN ID
            if 'Rx' in line and '0x' in line:
                count += 1
    
    return count


def main():
    log_file = 'VBG_CAN_Log__1_.log'
    
    print("=" * 60)
    print("Level 1: The Incident Report")
    print("=" * 60)
    print("\nCounting CAN messages...")
    
    total_messages = count_can_messages(log_file)
    
    print(f"\nTotal CAN messages: {total_messages:,}")
    print(f"\nAnswer: {total_messages}")
    
    # Verify the answer
    expected_answer = 38407
    if total_messages == expected_answer:
        print("✓ CORRECT! This matches the expected answer.")
    else:
        print(f"✗ Unexpected result. Expected: {expected_answer}")


if __name__ == '__main__':
    main()
