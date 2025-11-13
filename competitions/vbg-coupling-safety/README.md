# VBG Smart Coupling Safety Challenge

## Competition Overview

**Theme**: Automotive Safety Forensics - CAN Bus Analysis  
**Difficulty**: Intermediate  
**Domain**: Commercial Vehicle Safety Systems  
**Skills**: CAN protocol analysis, Signal decoding, Forensic investigation

## Background Story

You are a forensic analyst investigating a critical incident involving VBG Group's intelligent trailer coupling system. On March 11, 2025, at 11:38:07, a Volvo FH16 truck hauling a 40-ton refrigerated trailer experienced a sudden jack-knifing event on the E6 Highway near Göteborg, Sweden.

Thanks to VBG's advanced TE (Trailer Eyes) coupling system with integrated jack-knifing detection, the trailer remained securely attached, preventing what could have been a catastrophic multi-vehicle collision. However, the incident triggered multiple safety alarms and left critical questions unanswered.

Your mission is to analyze the CAN bus data log recovered from the vehicle's control modules to determine what happened and why.

## About VBG Group

VBG Group (vbg.eu) is a leading Nordic manufacturer of truck and trailer equipment, specializing in:
- Coupling and hitching systems
- Load securing solutions
- Smart safety technologies for commercial vehicles

The VBG TE (Trailer Eyes) system featured in this investigation represents the cutting edge of intelligent coupling technology, with:
- Real-time jack-knifing detection and warning
- Dual redundant coupling lock sensors
- Advanced drawbar angle monitoring
- Integrated safety control modules (BCM, CSM, DSM)

## System Components

### Control Modules
- **BCM** (Body Control Module): Overall vehicle coordination
- **CSM** (Coupling Safety Module): Manages trailer coupling locks
- **DSM** (Drawbar Stability Module): Monitors jack-knifing risk

### Key CAN Messages
- **JCKKNFNGSTS** (0xCF07731): Jack-knifing status and warnings
- **DBLLCKSNSR** (0xCF06523): Trailer-side coupling lock sensor
- **DBLLCKSNSRTRCK** (0xCF06931): Truck-side coupling lock sensor
- **DGTLJCKKNFNGSTS** (0xCF07623): Digital jack-knifing percentage

## Learning Objectives

Through this competition, you will:
1. Parse and analyze real-world CAN bus logs
2. Decode safety-critical vehicle signals using DBC specifications
3. Identify system anomalies and failure patterns
4. Establish forensic timelines from distributed data
5. Understand redundancy and fault-tolerance in safety systems

## Resources Provided

- **VBG_CAN_Log__1_.log**: Complete CAN bus capture from the incident
- **TE_CAN_DBC_V1_3.dbc**: CAN database specification for signal decoding
- This README with background information

## Challenge Structure

The competition consists of 5 progressive levels:

1. **Level 1**: Basic log analysis - Establish data scope
2. **Level 2**: Signal identification - Understand jack-knifing detection
3. **Level 3**: Anomaly detection - Discover coupling sensor failures
4. **Level 4**: Timeline reconstruction - Establish causal relationships
5. **Level 5**: Root cause analysis - Determine system-wide impact

## Tips for Success

- Study the DBC file to understand signal bit positions and value mappings
- Pay attention to CAN ID formats (extended IDs use 0x prefix with 8 hex digits)
- Timestamps in the log are in HH:MM:SS:MSMS format
- Look for patterns across multiple related messages
- Consider redundancy - VBG systems use multiple sensors for critical functions

## Real-World Impact

This type of forensic analysis is crucial for:
- Improving vehicle safety systems
- Meeting regulatory requirements (e.g., EU General Safety Regulation)
- Product liability investigations
- Continuous improvement in automotive engineering

Good luck, and remember: Your analysis will directly inform safety improvements that could save lives on Nordic highways!

---

**Competition ID**: b567c140-54e0-41a4-860f-45c4961b6d2c  
**Created**: November 2025  
**Industry Partner**: VBG Group AB
