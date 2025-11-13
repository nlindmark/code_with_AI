#!/usr/bin/env python3
"""
VBG Smart Coupling Safety Challenge - Level 2: The Warning Signs
Solution: Count jack-knifing detection system activation messages

Task: Count how many CAN messages with ID 0xCF07731 contain NON-ZERO data
      (indicating the jack-knifing detection system was actively monitoring)
Answer: 543
"""

def count_jackknifing_messages(log_file):
    """
    Count CAN messages with ID 0xCF07731 that have non-zero data.
    
    The jack-knifing status message (JCKKNFNGSTS) uses CAN ID 0xCF07731.
    - All zeros (00 00 00 00 00 00 00 00) = System in standby
    - Non-zero data = System actively monitoring critical angles
    """
    count = 0
    
    with open(log_file, 'r') as f:
        for line in f:
            # Look for messages with jack-knifing CAN ID
            if '0xCF07731' in line:
                # Extract the data bytes (everything after the CAN ID and type info)
                parts = line.strip().split()
                
                # Data bytes start after: Time, Rx, Channel, CAN_ID, Type, DLC
                # Example: 11:40:04:1372 Rx 1 0xCF07731 x 8 F8 72 4D 49 9A 01 01 00
                if len(parts) >= 14:  # Ensure we have data bytes
                    data_bytes = parts[6:14]  # Extract 8 data bytes
                    
                    # Check if ALL bytes are zero
                    all_zeros = all(byte == '00' for byte in data_bytes)
                    
                    # Count only non-zero messages (system active)
                    if not all_zeros:
                        count += 1
    
    return count


def main():
    # Level 2 uses the same log file from Level 1
    log_file = '../level1/VBG_CAN_Log__1_.log'
    
    print("=" * 60)
    print("Level 2: The Warning Signs")
    print("=" * 60)
    print("\nAnalyzing jack-knifing detection messages...")
    print("CAN ID: 0xCF07731 (JCKKNFNGSTS)")
    
    active_messages = count_jackknifing_messages(log_file)
    
    print(f"\nTotal 0xCF07731 messages with NON-ZERO data: {active_messages:,}")
    print(f"\nAnswer: {active_messages}")
    
    # Verify the answer
    expected_answer = 543
    if active_messages == expected_answer:
        print("✓ CORRECT! The jack-knifing detection system was active for 543 messages.")
    else:
        print(f"✗ Unexpected result. Expected: {expected_answer}")


if __name__ == '__main__':
    main()
