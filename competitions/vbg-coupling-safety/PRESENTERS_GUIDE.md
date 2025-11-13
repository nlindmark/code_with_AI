# VBG Smart Coupling Safety Challenge - Presenter's Guide

## Quick Start

**Competition Name**: VBG Smart Coupling Safety Challenge  
**Competition ID**: b567c140-54e0-41a4-860f-45c4961b6d2c  
**Duration**: 2-4 hours (depending on participant skill level)  
**Difficulty**: Intermediate  
**Participants**: Individual or teams of 2-3

## Story Hook (Opening Presentation)

*"March 11, 2025, 11:38 AM. A Volvo FH16 truck hauling 40 tons is merging onto the E6 Highway near Göteborg when disaster nearly strikes. A sudden jack-knifing event threatens to send the massive trailer careening into oncoming traffic. But thanks to VBG's intelligent coupling system, the trailer stays locked. Crisis averted. Or was it?*

*As forensic analysts, your job is to figure out what really happened by analyzing the black box - the CAN bus data log from the vehicle's control systems. Did the coupling system malfunction? Did it prevent the jack-knifing, or did something else trigger it? The answers are in the data."*

## Competition Format Options

### Option 1: Hackathon Style (2-3 hours)
- Teams compete to complete all 5 levels
- First team to complete all levels wins
- Hints available after 15 minutes of being stuck

### Option 2: Educational Workshop (3-4 hours)
- Guided progression through levels
- Instructor provides mini-lessons between levels
- Focus on learning CAN protocol and forensic techniques

### Option 3: Capture the Flag (CTF) (2-3 hours)
- Points for each level (100, 200, 300, 400, 500)
- Bonus points for speed
- Teams can work on any level in any order

## Level-by-Level Teaching Points

### Level 1: The Incident Report (15-20 minutes)
**Teaching Point**: CAN log structure and basic parsing
- Show header format: `Time Rx Channel CAN_ID Type DLC Data...`
- Explain difference between header lines and data lines
- Introduce command-line tools: `grep`, `wc`, `awk`

**Common Mistakes**:
- Counting header lines
- Not filtering for actual messages

**Hint Timing**: After 10 minutes if stuck

### Level 2: The Warning Signs (20-25 minutes)
**Teaching Point**: Message filtering and pattern recognition
- Explain CAN ID significance (0xCF07731 = jack-knifing status)
- Show how to filter by CAN ID
- Discuss normal vs. active states (all zeros vs. data)

**Common Mistakes**:
- Not understanding what "non-zero" means
- Filtering incorrectly

**Hint Timing**: After 12 minutes if stuck

### Level 3: The Coupling Anomaly (25-30 minutes)
**Teaching Point**: DBC file usage and signal decoding
- Open DBC file and locate DBLLCKSNSR definition
- Explain bit positions and value mappings
- Discuss why "Undefined" (0x03) is concerning

**Common Mistakes**:
- Looking at wrong byte position
- Not using DBC file for reference
- Hex vs. decimal confusion

**Hint Timing**: After 15 minutes if stuck

### Level 4: The Sequence of Events (30-35 minutes)
**Teaching Point**: Forensic timeline reconstruction
- Explain timestamp format (HH:MM:SS:MSMS)
- Show how to convert to comparable values
- Discuss causal relationships in data

**Common Mistakes**:
- Timestamp calculation errors
- Not finding FIRST occurrence
- Sign error (positive vs. negative)

**Hint Timing**: After 15 minutes if stuck

### Level 5: The Root Cause Report (30-40 minutes)
**Teaching Point**: System-level analysis and redundancy
- Explain concept of redundant sensors
- Show how to combine data from multiple sources
- Discuss implications for safety system design

**Common Mistakes**:
- Only counting one sensor
- Not understanding redundancy concept

**Hint Timing**: After 20 minutes if stuck

## Required Tools

### Minimum Setup
- Text editor (VS Code, Sublime, vim, nano)
- Command line (bash, zsh, PowerShell with WSL)
- Python 3.x (optional but recommended)

### Recommended Tools
- `grep` - for filtering
- `awk` - for column extraction
- `wc` - for counting
- Python with `cantools` library (for advanced parsing)

### Optional Tools
- Vector CANalyzer/CANoe (professional tools)
- Wireshark with CAN plugins
- Custom Python scripts

## Answer Key

| Level | Expected Answer | Common Wrong Answers |
|-------|----------------|---------------------|
| 1 | 38407 | 38428 (including headers) |
| 2 | 543 | 544 (off-by-one), variable (filtering error) |
| 3 | 93 | 186 (both sensors), 0 (wrong CAN ID) |
| 4 | 966 | -966 (wrong sign), various (timestamp calc errors) |
| 5 | 186 | 93 (only one sensor), 279 (triple counting) |

## Grading Rubric (If Scoring)

### Speed Bonus
- Level 1: < 15 min = +50 pts
- Level 2: < 20 min = +50 pts
- Level 3: < 25 min = +50 pts
- Level 4: < 30 min = +50 pts
- Level 5: < 35 min = +50 pts

### Methodology (Optional Bonus)
- Clean, documented code: +25 pts/level
- Creative approach: +25 pts/level
- Reusable tools created: +50 pts

## Wrap-Up Discussion Points

After completion, discuss:

1. **Technical Insights**:
   - How does CAN protocol work in modern vehicles?
   - Why is redundancy important in safety systems?
   - What makes a good forensic log?

2. **VBG-Specific**:
   - How does jack-knifing detection actually work?
   - What causes coupling sensors to fail?
   - How would you improve the system?

3. **Real-World Application**:
   - Similar investigations in automotive recalls
   - EU regulations requiring event data recorders
   - Career opportunities in automotive safety

4. **The Verdict**:
   *"The investigation revealed that extreme lateral forces during the emergency maneuver caused both redundant coupling sensors to temporarily malfunction. However, VBG's jack-knifing detection system functioned perfectly, maintaining coupling integrity and preventing a major accident. The incident has led to design improvements in sensor mounting to better withstand lateral forces."*

## Additional Resources

For participants who want to learn more:
- CAN Protocol basics: ISO 11898 standard
- J1939 protocol (used in commercial vehicles)
- VBG Group website: vbg.eu
- Automotive safety standards: ISO 26262

## Troubleshooting

**Q**: "I can't open the log file"  
**A**: It's a text file - use any text editor. Try: `less VBG_CAN_Log__1_.log`

**Q**: "What's a DBC file?"  
**A**: It's a CAN database that defines message structures. Open it in a text editor to see signal definitions.

**Q**: "My count is off by a few"  
**A**: Check your filtering logic. Are you including/excluding the right messages?

**Q**: "Timestamp math is confusing"  
**A**: Break it down: seconds × 1000 + milliseconds. Then subtract.

## Competition Variants

### For Beginners
- Provide pre-written Python scripts for parsing
- Give explicit byte positions
- Focus on concepts over tool usage

### For Advanced
- Remove hints entirely
- Add bonus challenges (e.g., plot jack-knifing angle over time)
- Require generating a formal incident report

### For Teams
- Assign roles: Parser, Analyst, Reporter
- Require collaboration and documentation
- Present findings to "VBG Safety Board"

---

**Setup Time**: 10-15 minutes  
**Competition Time**: 2-4 hours  
**Wrap-up**: 15-30 minutes  

Good luck running this competition! 🚚🔧
