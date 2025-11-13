# VBG Smart Coupling Safety Challenge - Competition Summary

## Story Overview

**Title**: The E6 Highway Incident - A CAN Bus Forensic Investigation

**Setting**: March 11, 2025, E6 Highway near Göteborg, Sweden

**Scenario**: A Volvo FH16 truck hauling a 40-ton refrigerated trailer experiences a sudden jack-knifing event. The VBG TE (Trailer Eyes) intelligent coupling system prevents disaster, but triggers multiple safety alarms. Players assume the role of forensic analysts investigating the CAN bus data to determine what happened.

## Competition Structure

**Competition ID**: b567c140-54e0-41a4-860f-45c4961b6d2c  
**Name**: VBG Smart Coupling Safety Challenge  
**Difficulty**: Intermediate  
**Total Levels**: 5

### Level Progression

**Level 1: The Incident Report**
- **Objective**: Count total CAN messages in the log
- **Answer**: 38,407 messages
- **Skills**: Basic log parsing, understanding CAN format
- **Story**: Establish the scope of data for investigation

**Level 2: The Warning Signs**
- **Objective**: Count jack-knifing detection activation messages
- **Answer**: 543 active monitoring messages
- **Skills**: Message filtering, identifying non-zero data patterns
- **Story**: Understand when the jack-knifing prevention system engaged

**Level 3: The Coupling Anomaly**
- **Objective**: Count "Undefined" coupling sensor states
- **Answer**: 93 undefined states
- **Skills**: Signal decoding using DBC, identifying anomalous values
- **Story**: Discover critical sensor failures during the incident

**Level 4: The Sequence of Events**
- **Objective**: Calculate time difference between sensor failure and jack-knifing
- **Answer**: 966 milliseconds
- **Skills**: Timestamp parsing, timeline reconstruction, forensic analysis
- **Story**: Determine if sensor failure caused or resulted from jack-knifing

**Level 5: The Root Cause Report**
- **Objective**: Count total undefined states across both redundant sensors
- **Answer**: 186 total undefined messages
- **Skills**: Multi-signal analysis, understanding redundancy
- **Story**: Determine severity of simultaneous redundant sensor failure

## Key Educational Elements

### Technical Skills Developed
1. **CAN Protocol Understanding**: Extended CAN IDs, message structure, data interpretation
2. **Signal Decoding**: Using DBC files to extract meaningful data from raw bytes
3. **Forensic Analysis**: Timeline reconstruction, causal relationship determination
4. **Safety Systems**: Understanding redundancy, fault tolerance, and fail-safe design

### VBG-Specific Features Highlighted
- **Jack-knifing Detection**: Real-time angle monitoring and warning systems
- **Dual Coupling Sensors**: Redundant safety design (CSM and BCM/DSM sensors)
- **Intelligent Coupling**: TE (Trailer Eyes) system capabilities
- **Safety Integration**: BCM, CSM, and DSM module coordination

### Real-World Relevance
- Automotive safety forensics
- EU General Safety Regulation compliance
- Product liability investigation techniques
- Continuous improvement in commercial vehicle safety

## Technical Details

### CAN Messages Used

| CAN ID | Name | Description | Module |
|--------|------|-------------|--------|
| 0xCF07731 | JCKKNFNGSTS | Jack-knifing status | DSM |
| 0xCF06523 | DBLLCKSNSR | Trailer coupling sensor | CSM |
| 0xCF06931 | DBLLCKSNSRTRCK | Truck coupling sensor | BCM |
| 0xCF07623 | DGTLJCKKNFNGSTS | Digital jack-knifing % | CSM |

### Signal Mappings

**DblLckSnsrRprtdSts** (Coupling Lock Status):
- 0 = Unlocked
- 1 = Locked
- 2 = Not present
- 3 = Undefined (ANOMALOUS)
- 4 = Inhibited

**JckKnfngSts** (Jack-knifing Status):
- 0 = Not Active
- 1 = Active (CRITICAL)

## Files Included

1. **Competition Structure**:
   - `config.json` - Competition metadata with UUID
   - `level1/` through `level5/` - Progressive challenges
   - Each level has `config.json` with problem statement

2. **Data Files**:
   - `VBG_CAN_Log__1_.log` - Real CAN bus capture (38,407 messages)
   - `TE_CAN_DBC_V1_3.dbc` - Signal specification database

3. **Documentation**:
   - `README.md` - Complete background and instructions
   - This summary document

## Story Arc

**Act 1** (Levels 1-2): Discovery
- Investigators establish data scope and identify safety system activation
- Introduces VBG's jack-knifing prevention technology

**Act 2** (Levels 3-4): Investigation
- Critical sensor anomalies discovered
- Timeline reveals sensor failure preceded jack-knifing
- Raises questions about causal relationships

**Act 3** (Level 5): Conclusion
- Redundant sensors both failed - design vulnerability identified
- Jack-knifing system functioned correctly despite sensor issues
- Analysis informs safety improvements for next-gen systems

## Deployment Instructions

1. Extract `vbg-coupling-safety.zip` to your competitions directory
2. Restart your competition server
3. The competition will auto-discover with UUID: b567c140-54e0-41a4-860f-45c4961b6d2c
4. Players can download the CAN log for analysis

## Educational Value

This competition bridges:
- **Computer Science**: Data parsing, signal processing, forensic analysis
- **Automotive Engineering**: CAN networks, safety systems, sensor redundancy
- **Real-World Application**: Actual VBG product technology and safety challenges

Perfect for:
- University automotive engineering programs
- Professional development in vehicle safety
- Hackathons focused on automotive technology
- Technical recruitment for automotive software roles

## Credits

**Company**: VBG Group AB (vbg.eu)  
**Industry**: Commercial Vehicle Equipment  
**Technology**: Trailer Eyes (TE) Intelligent Coupling System  
**Created**: November 2025

---

*This competition uses realistic scenarios based on VBG's actual coupling and jack-knifing prevention technology, demonstrating how CAN bus forensics can improve vehicle safety systems.*
