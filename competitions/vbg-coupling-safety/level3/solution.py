#!/usr/bin/env python3
"""
VBG Smart Coupling Safety Challenge - Level 3: The Coupling Anomaly
Solution: Count "Undefined" coupling sensor states

Task: Count how many times the coupling sensor (0xCF06523) reported 
      the anomalous "Undefined" (0x03) state
Answer: 93

According to DBC:
  BO_ 2364564771 DBLLCKSNSR: 8 CSM
  SG_ DblLckSnsrRprtdSts : 0|3@1+ (1,0) [0|5] "" BCM
  
  Values:
    0 = Unlocked
    1 = Locked
    2 = Not present
    3 = Undefined  ⚠️ (ANOMALOUS)
    4 = Inhibited
"""

def count_undefined_coupling_states(log_file):
    """
    Count messages where the coupling sensor reports "Undefined" (0x03).
    
    CAN ID: 0xCF06523 (DBLLCKSNSR - Double Lock Sensor)
    Signal: DblLckSnsrRprtdSts is at bits 0-2 of byte 0 (first data byte)
    Value 0x03 = Undefined state (should never occur in production)
    """
    count = 0
    
    with open(log_file, 'r') as f:
        for line in f:
            # Look for coupling sensor messages
            if '0xCF06523' in line:
                parts = line.strip().split()
                
                # Extract data bytes
                if len(parts) >= 14:
                    first_byte = parts[6]  # First data byte
                    
                    # Check if the value is 0x03 (Undefined)
                    if first_byte == '03':
                        count += 1
    
    return count


def analyze_coupling_states(log_file):
    """
    Additional analysis: Show all unique coupling sensor states.
    """
    states = {}
    state_names = {
        '00': 'Unlocked',
        '01': 'Locked',
        '02': 'Not present',
        '03': 'Undefined ⚠️',
        '04': 'Inhibited'
    }
    
    with open(log_file, 'r') as f:
        for line in f:
            if '0xCF06523' in line:
                parts = line.strip().split()
                if len(parts) >= 14:
                    first_byte = parts[6]
                    states[first_byte] = states.get(first_byte, 0) + 1
    
    return states, state_names


def main():
    log_file = '../level1/VBG_CAN_Log__1_.log'
    
    print("=" * 60)
    print("Level 3: The Coupling Anomaly")
    print("=" * 60)
    print("\nAnalyzing coupling sensor status messages...")
    print("CAN ID: 0xCF06523 (DBLLCKSNSR)")
    
    # Count undefined states
    undefined_count = count_undefined_coupling_states(log_file)
    
    # Additional analysis
    print("\n" + "-" * 60)
    print("Coupling Sensor State Distribution:")
    print("-" * 60)
    states, state_names = analyze_coupling_states(log_file)
    
    for state_code, count in sorted(states.items()):
        state_name = state_names.get(state_code, 'Unknown')
        marker = " ⚠️ ANOMALOUS" if state_code == '03' else ""
        print(f"  0x{state_code} ({state_name}): {count:,} messages{marker}")
    
    print("\n" + "=" * 60)
    print(f"Undefined (0x03) states: {undefined_count}")
    print(f"\nAnswer: {undefined_count}")
    
    # Verify the answer
    expected_answer = 93
    if undefined_count == expected_answer:
        print("✓ CORRECT! Found 93 anomalous 'Undefined' sensor states.")
    else:
        print(f"✗ Unexpected result. Expected: {expected_answer}")


if __name__ == '__main__':
    main()
