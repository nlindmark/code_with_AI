#!/usr/bin/env python3
"""
VBG Smart Coupling Safety Challenge - Level 4: The Sequence of Events
Solution: Calculate time difference between coupling anomaly and jack-knifing

Task: Calculate milliseconds between:
      - FIRST coupling sensor "Undefined" (0x03) on 0xCF06523
      - FIRST jack-knifing activation (non-zero) on 0xCF07731
Answer: 966 milliseconds

Time format: HH:MM:SS:MSMS (e.g., 11:40:03:1406)
Formula: (Jack-knifing timestamp) - (Coupling anomaly timestamp)
"""

def parse_timestamp(timestamp_str):
    """
    Parse timestamp from format HH:MM:SS:MSMS to total milliseconds.
    
    Example: "11:40:03:1406" means:
      - 11 hours = 11 * 3600 * 1000 ms
      - 40 minutes = 40 * 60 * 1000 ms
      - 3 seconds = 3 * 1000 ms
      - 1406 milliseconds = 1406 ms
    """
    parts = timestamp_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    milliseconds = int(parts[3])
    
    total_ms = (hours * 3600 * 1000) + (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
    return total_ms


def find_first_coupling_anomaly(log_file):
    """
    Find the first occurrence of coupling sensor reporting Undefined (0x03).
    """
    with open(log_file, 'r') as f:
        for line in f:
            if '0xCF06523' in line:
                parts = line.strip().split()
                if len(parts) >= 14:
                    first_byte = parts[6]
                    if first_byte == '03':
                        timestamp = parts[0]  # First column is timestamp
                        return timestamp, line.strip()
    return None, None


def find_first_jackknifing_activation(log_file):
    """
    Find the first occurrence of jack-knifing detection with non-zero data.
    """
    with open(log_file, 'r') as f:
        for line in f:
            if '0xCF07731' in line:
                parts = line.strip().split()
                if len(parts) >= 14:
                    data_bytes = parts[6:14]
                    all_zeros = all(byte == '00' for byte in data_bytes)
                    
                    if not all_zeros:
                        timestamp = parts[0]
                        return timestamp, line.strip()
    return None, None


def main():
    log_file = '../level1/VBG_CAN_Log__1_.log'
    
    print("=" * 60)
    print("Level 4: The Sequence of Events")
    print("=" * 60)
    print("\nForensic Timeline Reconstruction...")
    
    # Find first coupling anomaly
    coupling_time_str, coupling_line = find_first_coupling_anomaly(log_file)
    print(f"\n1. FIRST Coupling Sensor Anomaly (0xCF06523 = 0x03):")
    print(f"   Timestamp: {coupling_time_str}")
    print(f"   Line: {coupling_line[:80]}...")
    
    # Find first jack-knifing activation
    jackknife_time_str, jackknife_line = find_first_jackknifing_activation(log_file)
    print(f"\n2. FIRST Jack-knifing Detection Activation (0xCF07731 non-zero):")
    print(f"   Timestamp: {jackknife_time_str}")
    print(f"   Line: {jackknife_line[:80]}...")
    
    # Calculate time difference
    coupling_ms = parse_timestamp(coupling_time_str)
    jackknife_ms = parse_timestamp(jackknife_time_str)
    
    time_diff = jackknife_ms - coupling_ms
    
    print("\n" + "=" * 60)
    print("Timeline Analysis:")
    print("=" * 60)
    print(f"Coupling anomaly at:    {coupling_time_str} ({coupling_ms:,} ms total)")
    print(f"Jack-knifing started:   {jackknife_time_str} ({jackknife_ms:,} ms total)")
    print(f"\nTime difference: {time_diff} milliseconds")
    
    # Interpretation
    print("\n" + "-" * 60)
    print("Interpretation:")
    print("-" * 60)
    if time_diff > 0:
        print(f"✓ Coupling sensor anomaly occurred FIRST")
        print(f"  Jack-knifing detection activated {time_diff}ms later")
        print(f"  This suggests the coupling issue may have contributed to the incident.")
    else:
        print(f"✓ Jack-knifing occurred FIRST")
        print(f"  Coupling sensor anomaly appeared {abs(time_diff)}ms later")
        print(f"  This suggests the jack-knifing may have caused sensor stress.")
    
    print(f"\nAnswer: {time_diff}")
    
    # Verify the answer
    expected_answer = 966
    if time_diff == expected_answer:
        print("✓ CORRECT! The coupling anomaly preceded jack-knifing by 966ms.")
    else:
        print(f"✗ Unexpected result. Expected: {expected_answer}")


if __name__ == '__main__':
    main()
