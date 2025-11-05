# Fibonacci Challenge - AI Competition

A 4-level coding competition focused on the Fibonacci sequence, progressing from basic calculations to advanced pattern recognition.

## Competition Overview

**Competition ID:** 1  
**Name:** Fibonacci Challenge  
**Theme:** Master the famous Fibonacci sequence through progressively challenging problems

## Level Breakdown

### Level 1: Fibonacci Basics
**Difficulty:** Easy  
**Concept:** Basic Fibonacci calculation  
**Challenge:** Calculate the 10th Fibonacci number (F(10))  
**Answer:** 55

### Level 2: Even Fibonacci Sum
**Difficulty:** Medium  
**Concept:** Filtering and aggregation  
**Challenge:** Sum all even Fibonacci numbers from F(0) to F(20)  
**Answer:** 3382

### Level 3: Fibonacci Indices Challenge
**Difficulty:** Medium-Hard  
**Concept:** File processing and lookup  
**Challenge:** Read indices from a file, calculate Fibonacci numbers at those indices, and sum them  
**Input File:** indices.txt (contains: 15, 25, 30, 12, 18)  
**Answer:** 910403

### Level 4: The Golden Ratio Challenge
**Difficulty:** Hard  
**Concept:** Mathematical patterns and precision  
**Challenge:** Count how many consecutive Fibonacci number ratios round to exactly 1.618 (3 decimal places) from F(1) to F(50)  
**Answer:** 41

## Directory Structure

```
fibonacci-competition/
├── config.json                    # Competition metadata
├── level1/
│   ├── config.json               # Level 1 configuration
│   └── solution.py               # Reference solution
├── level2/
│   ├── config.json               # Level 2 configuration
│   └── solution.py               # Reference solution
├── level3/
│   ├── config.json               # Level 3 configuration
│   ├── indices.txt               # Input file with Fibonacci indices
│   └── solution.py               # Reference solution
├── level4/
│   ├── config.json               # Level 4 configuration
│   └── solution.py               # Reference solution
└── README.md                      # This file
```

## Installation Instructions

1. **Copy to competitions directory:**
   ```bash
   cp -r fibonacci-competition /path/to/your/competitions/competition1/
   ```

2. **Verify structure:**
   ```bash
   cd /path/to/your/competitions/competition1
   ls -R
   ```

3. **Test solutions (optional):**
   ```bash
   python3 level1/solution.py
   python3 level2/solution.py
   python3 level3/solution.py
   python3 level4/solution.py
   ```

4. **Restart your competition server**
   The competition will be auto-discovered and loaded on startup.

## Educational Objectives

This competition teaches:
- **Algorithm implementation:** Iterative Fibonacci calculation
- **Data filtering:** Selecting elements based on conditions
- **File I/O:** Reading and processing input files
- **Mathematical analysis:** Understanding the Golden Ratio convergence
- **Precision handling:** Working with floating-point rounding

## The Fibonacci Sequence

The Fibonacci sequence is defined as:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) for n ≥ 2

**Sequence:** 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377...

**The Golden Ratio (φ):** As n increases, the ratio F(n+1)/F(n) converges to φ ≈ 1.618033988749895

## Tips for Participants

1. **Level 1:** Start simple, implement a basic iterative solution
2. **Level 2:** Remember that every third Fibonacci number is even
3. **Level 3:** Parse the input file carefully and calculate each Fibonacci number
4. **Level 4:** Pay attention to rounding rules - round to 3 decimal places before comparing

## Validation

All answers have been verified with the provided solution scripts:
- ✅ Level 1: 55
- ✅ Level 2: 3382
- ✅ Level 3: 910403
- ✅ Level 4: 41

## License

This competition is free to use for educational purposes.
