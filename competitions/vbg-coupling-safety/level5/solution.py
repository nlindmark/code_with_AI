#!/usr/bin/env python3
"""
VBG Smart Coupling Safety Challenge - Level 5: The Root Cause Report
Solution: Count total Undefined states across BOTH redundant coupling sensors

Task: Calculate TOTAL "Undefined" (0x03) states across:
      - CSM Sensor (0xCF06523): DBLLCKSNSR - Trailer-side
      - BCM/DSM Sensor (0xCF06931): DBLLCKSNSRTRCK - Truck-side
Answer: 186 (93 + 93)

This reveals that BOTH redundant sensors failed simultaneously - a critical
design vulnerability where extreme lateral forces affected both sensors.
"""

def count_sensor_undefined_states(log_file, can_id):
    """
    Count Undefined (0x03) states for a specific coupling sensor.
    """
    count = 0
    timestamps = []
    
    with open(log_file, 'r') as f:
        for line in f:
            if can_id in line:
                parts = line.strip().split()
                if len(parts) >= 14:
                    first_byte = parts[6]
                    if first_byte == '03':
                        count += 1
                        timestamps.append(parts[0])
    
    return count, timestamps


def analyze_redundancy_failure(log_file):
    """
    Comprehensive analysis of both coupling sensors.
    """
    print("=" * 60)
    print("REDUNDANT SENSOR ANALYSIS")
    print("=" * 60)
    
    # Analyze CSM sensor (trailer-side)
    csm_count, csm_times = count_sensor_undefined_states(log_file, '0xCF06523')
    print(f"\n1. CSM Sensor (0xCF06523) - DBLLCKSNSR")
    print(f"   Location: Trailer-side coupling lock sensor")
    print(f"   Undefined states: {csm_count}")
    if csm_times:
        print(f"   First failure: {csm_times[0]}")
        print(f"   Last failure:  {csm_times[-1]}")
    
    # Analyze BCM/DSM sensor (truck-side)
    bcm_count, bcm_times = count_sensor_undefined_states(log_file, '0xCF06931')
    print(f"\n2. BCM/DSM Sensor (0xCF06931) - DBLLCKSNSRTRCK")
    print(f"   Location: Truck-side coupling sensor")
    print(f"   Undefined states: {bcm_count}")
    if bcm_times:
        print(f"   First failure: {bcm_times[0]}")
        print(f"   Last failure:  {bcm_times[-1]}")
    
    return csm_count, bcm_count, csm_times, bcm_times


def main():
    log_file = '../level1/VBG_CAN_Log__1_.log'
    
    print("=" * 60)
    print("Level 5: The Root Cause Report")
    print("=" * 60)
    print("\nAnalyzing redundant coupling sensor failures...")
    
    # Comprehensive analysis
    csm_count, bcm_count, csm_times, bcm_times = analyze_redundancy_failure(log_file)
    
    # Calculate total
    total_undefined = csm_count + bcm_count
    
    # Critical findings
    print("\n" + "=" * 60)
    print("CRITICAL FINDINGS")
    print("=" * 60)
    print(f"\nTotal Undefined states across BOTH sensors: {total_undefined}")
    print(f"  - Trailer-side (CSM):  {csm_count}")
    print(f"  - Truck-side (BCM):    {bcm_count}")
    
    # Safety implications
    print("\n" + "-" * 60)
    print("Safety System Implications:")
    print("-" * 60)
    
    if csm_count > 0 and bcm_count > 0:
        print("⚠️  REDUNDANCY FAILURE DETECTED")
        print("   Both independent sensors reported Undefined states")
        print("   This indicates a common-mode failure scenario")
        print()
        print("   Likely cause: Extreme lateral forces during jack-knifing")
        print("   affected BOTH sensors simultaneously, defeating the")
        print("   redundancy design.")
        print()
        print("   Recommendation: Review sensor mounting design to better")
        print("   isolate sensors from lateral stress loads.")
    else:
        print("✓  Redundancy maintained - only one sensor affected")
    
    # Compare timing
    if csm_times and bcm_times:
        from datetime import datetime
        print("\n" + "-" * 60)
        print("Temporal Correlation:")
        print("-" * 60)
        print(f"CSM first failure:  {csm_times[0]}")
        print(f"BCM first failure:  {bcm_times[0]}")
        
        if csm_times[0] == bcm_times[0]:
            print("⚠️  SIMULTANEOUS FAILURE - sensors failed at same instant")
        else:
            print("   Sensors failed at different times (cascade effect)")
    
    print("\n" + "=" * 60)
    print(f"Answer: {total_undefined}")
    
    # Verify the answer
    expected_answer = 186
    if total_undefined == expected_answer:
        print("✓ CORRECT! Both redundant sensors experienced 186 total failures.")
        print("\n" + "=" * 60)
        print("INVESTIGATION COMPLETE")
        print("=" * 60)
        print("\nConclusion: The VBG TE jack-knifing detection system functioned")
        print("correctly and prevented trailer separation. However, extreme")
        print("lateral forces caused simultaneous failure of both coupling")
        print("sensors - revealing a design vulnerability that requires review.")
        print("\nRecommendation: Improve sensor isolation and add tertiary")
        print("verification through IMU-based angle monitoring.")
    else:
        print(f"✗ Unexpected result. Expected: {expected_answer}")


if __name__ == '__main__':
    main()
