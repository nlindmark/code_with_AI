# VBG Smart Coupling Safety Challenge - Solutions Guide

## Overview

This document provides complete solutions for all 5 levels of the VBG Smart Coupling Safety Challenge, with multiple approaches (Python, Bash, command-line) and detailed explanations.

---

## Level 1: The Incident Report

### Challenge
Count the total number of CAN messages recorded during the incident.

### Answer: 38,407

### Approach 1: Python Solution
```python
def count_can_messages(log_file):
    count = 0
    with open(log_file, 'r') as f:
        for line in f:
            if 'Rx' in line and '0x' in line:
                count += 1
    return count
```

**Explanation:** 
- CAN messages are lines containing "Rx" (received) and "0x" (CAN ID in hex)
- Skip header lines that start with "***"
- Count all data lines

### Approach 2: Bash One-liner
```bash
grep -E 'Rx [0-9]+ 0x' VBG_CAN_Log__1_.log | wc -l
```

**Explanation:**
- `grep -E` uses extended regex
- `Rx [0-9]+ 0x` matches the CAN message pattern
- `wc -l` counts lines

### Approach 3: AWK
```bash
awk '/Rx.*0x/ {count++} END {print count}' VBG_CAN_Log__1_.log
```

### Common Mistakes
- ❌ Counting header lines (lines starting with ***)
- ❌ Including blank lines
- ✓ Only count actual message lines with Rx and 0x

### Learning Points
- CAN log format: Time Rx Channel CAN_ID Type DLC Data...
- Importance of filtering non-data lines
- Basic text processing techniques

---

## Level 2: The Warning Signs

### Challenge
Count CAN messages with ID 0xCF07731 that have NON-ZERO data (jack-knifing detection active).

### Answer: 543

### Approach 1: Python Solution
```python
def count_jackknifing_messages(log_file):
    count = 0
    with open(log_file, 'r') as f:
        for line in f:
            if '0xCF07731' in line:
                parts = line.strip().split()
                if len(parts) >= 14:
                    data_bytes = parts[6:14]  # 8 data bytes
                    all_zeros = all(byte == '00' for byte in data_bytes)
                    if not all_zeros:
                        count += 1
    return count
```

**Explanation:**
- Filter for CAN ID 0xCF07731 (JCKKNFNGSTS)
- Extract 8 data bytes (positions 6-13 in split line)
- Check if all bytes are '00' (inactive state)
- Count only non-zero messages (active monitoring)

### Approach 2: Bash One-liner
```bash
grep '0xCF07731' VBG_CAN_Log__1_.log | grep -v '00 00 00 00 00 00 00 00' | wc -l
```

**Explanation:**
- First grep finds all jack-knifing messages
- `grep -v` excludes lines with all zeros
- Result is count of active messages

### Approach 3: AWK with Logic
```bash
awk '/0xCF07731/ && !/00 00 00 00 00 00 00 00/ {count++} END {print count}' VBG_CAN_Log__1_.log
```

### Common Mistakes
- ❌ Counting ALL 0xCF07731 messages (including zeros)
- ❌ Not understanding what "non-zero" means
- ✓ Only count messages where system is actively monitoring

### Learning Points
- CAN ID 0xCF07731 = Jack-knifing Status (JCKKNFNGSTS)
- All zeros = standby mode, non-zero = active monitoring
- Pattern matching and negative filtering

---

## Level 3: The Coupling Anomaly

### Challenge
Count how many times coupling sensor (0xCF06523) reported "Undefined" (0x03) state.

### Answer: 93

### Approach 1: Python Solution
```python
def count_undefined_coupling_states(log_file):
    count = 0
    with open(log_file, 'r') as f:
        for line in f:
            if '0xCF06523' in line:
                parts = line.strip().split()
                if len(parts) >= 14:
                    first_byte = parts[6]  # First data byte
                    if first_byte == '03':
                        count += 1
    return count
```

**Explanation:**
- Filter for CAN ID 0xCF06523 (DBLLCKSNSR - Double Lock Sensor)
- Extract first data byte (position 6)
- Check if it equals '03' (Undefined state)
- According to DBC: 0=Unlocked, 1=Locked, 2=Not present, 3=Undefined, 4=Inhibited

### Approach 2: Bash One-liner
```bash
grep '0xCF06523' VBG_CAN_Log__1_.log | grep '03 00 00 00 00 00 00 00' | wc -l
```

**Explanation:**
- Find all coupling sensor messages
- Filter for those with 0x03 as first byte
- The rest of bytes are zeros in this specific case

### Approach 3: Using DBC Knowledge
```bash
# More robust version checking only first byte position
grep '0xCF06523' VBG_CAN_Log__1_.log | awk '$7 == "03" {count++} END {print count}'
```

### Common Mistakes
- ❌ Looking at wrong byte position
- ❌ Not using DBC file to understand signal mapping
- ❌ Counting other sensors (0xCF06931)
- ✓ Only count first data byte value of 0x03

### Learning Points
- CAN ID 0xCF06523 = DBLLCKSNSR (trailer-side coupling sensor)
- DBC files define signal bit positions and value mappings
- "Undefined" (0x03) is an anomalous failure state
- Bit position: Signal starts at bit 0, length 3 bits (can represent 0-7)

### DBC Reference
```
BO_ 2364564771 DBLLCKSNSR: 8 CSM
 SG_ DblLckSnsrRprtdSts : 0|3@1+ (1,0) [0|5] "" BCM

VAL_ 2364564771 DblLckSnsrRprtdSts 
  0 "Unlocked" 
  1 "Locked" 
  2 "Not present" 
  3 "Undefined"   ← ANOMALOUS
  4 "Inhibited" ;
```

---

## Level 4: The Sequence of Events

### Challenge
Calculate time difference in milliseconds between first coupling anomaly and first jack-knifing activation.

### Answer: 966 milliseconds

### Approach 1: Python Solution
```python
def parse_timestamp(timestamp_str):
    """Convert HH:MM:SS:MSMS to total milliseconds."""
    parts = timestamp_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    milliseconds = int(parts[3])
    
    total_ms = (hours * 3600 * 1000) + (minutes * 60 * 1000) + 
               (seconds * 1000) + milliseconds
    return total_ms

def find_first_coupling_anomaly(log_file):
    with open(log_file, 'r') as f:
        for line in f:
            if '0xCF06523' in line:
                parts = line.strip().split()
                if len(parts) >= 14 and parts[6] == '03':
                    return parts[0]  # timestamp
    return None

def find_first_jackknifing(log_file):
    with open(log_file, 'r') as f:
        for line in f:
            if '0xCF07731' in line:
                parts = line.strip().split()
                if len(parts) >= 14:
                    data_bytes = parts[6:14]
                    if not all(b == '00' for b in data_bytes):
                        return parts[0]  # timestamp
    return None

# Main calculation
coupling_time = find_first_coupling_anomaly(log_file)
jackknife_time = find_first_jackknifing(log_file)

coupling_ms = parse_timestamp(coupling_time)
jackknife_ms = parse_timestamp(jackknife_time)

difference = jackknife_ms - coupling_ms
```

**Explanation:**
- Find first occurrence of coupling sensor Undefined (0xCF06523 with 0x03)
- Find first occurrence of jack-knifing activation (0xCF07731 non-zero)
- Parse timestamps: 11:40:03:1406 = 3 seconds + 1406 ms = 4406 ms (within that minute)
- Calculate difference: 5372 ms - 4406 ms = 966 ms

### Approach 2: Manual Bash Calculation
```bash
# Find first coupling anomaly
COUPLING=$(grep '0xCF06523' VBG_CAN_Log__1_.log | grep '03 00 00 00' | head -1)
# Result: 11:40:03:1406

# Find first jack-knifing
JACKKNIFE=$(grep '0xCF07731' VBG_CAN_Log__1_.log | grep -v '00 00 00 00 00 00 00 00' | head -1)
# Result: 11:40:04:1372

# Manual calculation:
# Coupling:    3 seconds * 1000 + 1406 = 4406 ms
# Jack-knife:  4 seconds * 1000 + 1372 = 5372 ms
# Difference:  5372 - 4406 = 966 ms
```

### Approach 3: Python One-liner with Timestamps
```python
import re
from datetime import datetime

log_file = 'VBG_CAN_Log__1_.log'

# Find timestamps
with open(log_file) as f:
    lines = f.readlines()
    
coupling_ts = next(l.split()[0] for l in lines if '0xCF06523' in l and '03 00 00 00' in l)
jackknife_ts = next(l.split()[0] for l in lines if '0xCF07731' in l and '00 00 00 00 00 00 00 00' not in l)

# Parse: HH:MM:SS:MSMS
c_parts = coupling_ts.split(':')
j_parts = jackknife_ts.split(':')

c_ms = int(c_parts[2]) * 1000 + int(c_parts[3])
j_ms = int(j_parts[2]) * 1000 + int(j_parts[3])

# Add minute difference if needed
if int(j_parts[2]) < int(c_parts[2]):  # Minute rolled over
    j_ms += 60000

diff = j_ms - c_ms
print(f"Difference: {diff} ms")
```

### Common Mistakes
- ❌ Not finding FIRST occurrence (using wrong search)
- ❌ Timestamp parsing errors (forgetting seconds are in position 2)
- ❌ Sign error (subtracting in wrong order)
- ❌ Not converting to common time base
- ✓ Parse timestamps correctly and find FIRST of each event

### Learning Points
- Forensic timeline reconstruction from logs
- Timestamp format: HH:MM:SS:MSMS (last 4 digits are milliseconds)
- Finding first occurrence vs. counting all occurrences
- Determining causal relationships from temporal order
- If coupling failed BEFORE jack-knifing, it may have contributed to the incident

### Timeline Interpretation
```
11:40:03:1406  ← Coupling sensor reports "Undefined"
       ↓
   [966 ms]    ← Critical window
       ↓
11:40:04:1372  ← Jack-knifing detection activates

Conclusion: Coupling sensor anomaly PRECEDED jack-knifing,
suggesting sensor failure may have contributed to the incident.
```

---

## Level 5: The Root Cause Report

### Challenge
Count TOTAL "Undefined" (0x03) states across BOTH redundant coupling sensors.

### Answer: 186 (93 + 93)

### Approach 1: Python Solution
```python
def count_sensor_failures(log_file, can_id):
    count = 0
    with open(log_file, 'r') as f:
        for line in f:
            if can_id in line:
                parts = line.strip().split()
                if len(parts) >= 14 and parts[6] == '03':
                    count += 1
    return count

# Count both sensors
csm_count = count_sensor_failures(log_file, '0xCF06523')  # Trailer-side
bcm_count = count_sensor_failures(log_file, '0xCF06931')  # Truck-side

total = csm_count + bcm_count
print(f"Total redundancy failures: {total}")
```

**Explanation:**
- VBG system has TWO coupling sensors for redundancy:
  - 0xCF06523 (DBLLCKSNSR) - Trailer-side CSM sensor
  - 0xCF06931 (DBLLCKSNSRTRCK) - Truck-side BCM/DSM sensor
- Count Undefined (0x03) states from BOTH sensors
- Total reveals simultaneous redundancy failure

### Approach 2: Bash One-liner
```bash
echo $(($(grep '0xCF06523' VBG_CAN_Log__1_.log | grep '03 00 00 00' | wc -l) + \
         $(grep '0xCF06931' VBG_CAN_Log__1_.log | grep '03 00 00 00' | wc -l)))
```

### Approach 3: Combined Grep
```bash
grep -E '0xCF06523|0xCF06931' VBG_CAN_Log__1_.log | grep '03 00 00 00' | wc -l
```

**Explanation:**
- `grep -E` with alternation matches either CAN ID
- Filter for 0x03 (Undefined) as first byte
- Count all matches

### Common Mistakes
- ❌ Only counting one sensor (Level 3 answer: 93)
- ❌ Triple-counting by including other sensors
- ❌ Not understanding redundancy concept
- ✓ Count BOTH sensors: 93 + 93 = 186

### Learning Points
- **Redundancy in safety systems**: Two independent sensors
- **Common-mode failure**: Both sensors failed simultaneously
- **Design vulnerability**: Lateral forces affected both sensors
- **Safety implications**: Redundancy defeated by shared failure mode

### System Architecture
```
VBG TE Coupling System
  ├── CSM (Coupling Safety Module)
  │   └── Sensor 0xCF06523 (DBLLCKSNSR)
  │       └── Location: Trailer-side coupling lock
  │       └── Failures: 93 Undefined states
  │
  └── BCM/DSM (Body/Drawbar Stability Modules)
      └── Sensor 0xCF06931 (DBLLCKSNSRTRCK)
          └── Location: Truck-side coupling
          └── Failures: 93 Undefined states

Total Redundancy Failure: 186 events
```

### Safety Analysis
**Normal Operation:**
- If CSM sensor fails → BCM sensor provides backup
- If BCM sensor fails → CSM sensor provides backup
- ✓ System maintains coupling verification

**Incident Condition:**
- BOTH sensors report Undefined simultaneously
- Redundancy defeated by common-mode failure
- ✗ Design vulnerability revealed

**Root Cause:**
Extreme lateral forces during jack-knifing affected BOTH sensor mountings, causing simultaneous electrical/mechanical disturbances.

**Recommendation:**
- Improve sensor mounting isolation
- Add tertiary verification (IMU-based angle sensing)
- Review sensor placement to avoid common stress points

---

## Complete Solutions Summary

| Level | Challenge | Answer | Key CAN IDs | Primary Skill |
|-------|-----------|--------|-------------|---------------|
| 1 | Count total messages | 38,407 | All | Log parsing |
| 2 | Jack-knifing activations | 543 | 0xCF07731 | Pattern filtering |
| 3 | Coupling anomalies | 93 | 0xCF06523 | DBC decoding |
| 4 | Timeline difference | 966 ms | 0xCF06523, 0xCF07731 | Forensic analysis |
| 5 | Total redundancy failures | 186 | 0xCF06523, 0xCF06931 | System analysis |

---

## Running the Solutions

### Python Solutions (Individual Levels)
```bash
cd level1
python3 solution.py

cd ../level2
python3 solution.py

# ... etc
```

### All Python Solutions at Once
```bash
python3 run_all_solutions.py
```

### Bash Solutions (All Levels)
```bash
chmod +x bash_solutions.sh
./bash_solutions.sh
```

### Quick Command-Line Solutions
```bash
# Level 1
grep -E 'Rx [0-9]+ 0x' level1/VBG_CAN_Log__1_.log | wc -l

# Level 2
grep '0xCF07731' level1/VBG_CAN_Log__1_.log | grep -v '00 00 00 00 00 00 00 00' | wc -l

# Level 3
grep '0xCF06523' level1/VBG_CAN_Log__1_.log | grep '03 00 00 00' | wc -l

# Level 4 (requires calculation)
# First coupling: grep '0xCF06523' ... | grep '03 00 00 00' | head -1
# First jackknife: grep '0xCF07731' ... | grep -v '00 00 00 00 00 00 00 00' | head -1
# Calculate: (4*1000+1372) - (3*1000+1406) = 966

# Level 5
echo $(($(grep '0xCF06523' level1/VBG_CAN_Log__1_.log | grep '03 00 00 00' | wc -l) + $(grep '0xCF06931' level1/VBG_CAN_Log__1_.log | grep '03 00 00 00' | wc -l)))
```

---

## Advanced Analysis (Bonus)

### Visualizing Jack-knifing Over Time
```python
import matplotlib.pyplot as plt

timestamps = []
angles = []

with open('level1/VBG_CAN_Log__1_.log') as f:
    for line in f:
        if '0xCF07731' in line:
            parts = line.split()
            time_parts = parts[0].split(':')
            seconds = int(time_parts[2]) + int(time_parts[3]) / 1000
            timestamps.append(seconds)
            
            # Decode angle from data bytes (simplified)
            if parts[6] != '00' or parts[7] != '00':
                angles.append(1)  # Active
            else:
                angles.append(0)  # Inactive

plt.plot(timestamps, angles)
plt.xlabel('Time (seconds)')
plt.ylabel('Jack-knifing Detection Active')
plt.title('VBG Jack-knifing Detection Timeline')
plt.show()
```

### Redundancy Failure Timeline
```python
csm_failures = []
bcm_failures = []

with open('level1/VBG_CAN_Log__1_.log') as f:
    for line in f:
        parts = line.split()
        timestamp = parts[0]
        
        if '0xCF06523' in line and parts[6] == '03':
            csm_failures.append(timestamp)
        elif '0xCF06931' in line and parts[6] == '03':
            bcm_failures.append(timestamp)

print(f"CSM first failure: {csm_failures[0]}")
print(f"BCM first failure: {bcm_failures[0]}")
print(f"Simultaneous: {csm_failures[0] == bcm_failures[0]}")
```

---

## Tools Reference

### Essential Command-Line Tools
- `grep`: Filter lines matching patterns
- `wc -l`: Count lines
- `awk`: Text processing and calculations
- `head`/`tail`: Get first/last N lines
- `sort`/`uniq`: Sort and deduplicate

### Python Libraries
- Built-in: `re`, `datetime`
- Optional: `cantools` (for DBC parsing)
- Optional: `matplotlib` (for visualization)

### Professional Tools (Optional)
- Vector CANalyzer/CANoe
- Wireshark with CAN plugins
- PCAN-View

---

## Conclusion

The VBG Smart Coupling Safety Challenge demonstrates real-world automotive forensics through CAN bus analysis. The progressive difficulty teaches:

1. **Basic skills**: Log parsing, pattern matching
2. **Protocol knowledge**: CAN format, message structure
3. **Domain expertise**: DBC files, signal decoding
4. **Forensic techniques**: Timeline reconstruction, causality
5. **Systems thinking**: Redundancy, failure modes, safety design

The investigation reveals that while VBG's jack-knifing detection system performed correctly, the redundant coupling sensors experienced a common-mode failure due to extreme lateral forces - a valuable lesson in safety system design.

**Final Verdict:** System worked as designed, but design improvement needed for next-generation systems.
