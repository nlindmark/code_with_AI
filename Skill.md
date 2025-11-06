---
name: ai-competition-directory-builder
description: "Create and validate competition directory structures for Code with AI system, including config.json files with UUID-based competition IDs. Each competition should have a UUID in config.json. Competitions should be saved as downloadable zip files ready for deployment."
---

## Core Instructions for Claude

You are an expert assistant helping users create competition directories for a Code with AI competition system. When users ask about creating competitions, you should:

1. **Guide them through the process step-by-step**
2. **Provide exact folder structures and naming conventions**
3. **Generate config.json files with correct JSON syntax**
4. **Help validate their structure against requirements**
5. **Provide examples and templates they can use**

Always verify that:
- Competition folders can have any name (no strict pattern required)
- Each competition should have a UUID in config.json (will be auto-generated if missing)
- JSON files are valid and complete
- Required fields are present
- Optional files are properly referenced
- Competitions should be created as zip files for easy download and deployment

---

## Directory Structure

### Required Structure
```
competitions/
└── {any-folder-name}/            # Any folder name allowed (e.g., competition1, my-comp, external-2024)
    ├── config.json              # REQUIRED: Competition metadata with UUID id
    ├── Summary.md               # REQUIRED: Competition summary for AI engine
    └── level{M}/                # REQUIRED: At least one level (M starts at 1)
        ├── config.json          # REQUIRED: Level configuration
        ├── solution.py          # OPTIONAL: Reference solution
        └── {input_file}         # OPTIONAL: Any input data file
```

---

## Naming Rules

### Competition Folders
- **Pattern**: Any folder name is allowed
- **Valid**: `competition1`, `competition2`, `my-competition`, `external-2024`, `fibonacci-challenge`
- **Note**: Folder names are flexible - use descriptive names that make sense for your competitions
- **Important**: The competition ID is stored in `config.json` as a UUID, not derived from folder name

### Level Folders
- **Pattern**: `level{N}` where N starts at 1
- **Valid**: `level1`, `level2`, `level3`
- **Invalid**: `level-1`, `Level1`, `level_one`
- **Note**: Should be sequential (level1, level2, level3...)

### Input Files
- **Pattern**: Any valid filename
- **Examples**: `input.txt`, `data.csv`, `api_stub.json`, `VBG_CAN_Log.log`
- **Note**: Must exactly match filename in config.json

---

## Configuration Files

### Competition config.json

**Location**: `competitions/{folder-name}/config.json`

**Required Fields**:
```json
{
  "id": "<uuid>",          // UUID string (auto-generated if missing, e.g., "aa182b36-0e7d-434b-b320-ae3570126ccc")
  "name": "<string>",      // Display name
  "description": "<string>"  // Brief description
}
```

**Example**:
```json
{
  "id": "1029bb53-31e5-4e35-8d13-b0da3e20091b",
  "name": "Fibonacci Challenge",
  "description": "Master the famous Fibonacci sequence through progressively challenging problems"
}
```

**Note**: The `id` field should be a UUID string. If `id` is missing, a UUID will be auto-generated when the competition is loaded, but it's recommended to include it explicitly in the config.json for consistency and proper tracking.

### Level config.json

**Location**: `competitions/{folder-name}/level{M}/config.json`

**Required Fields**:
```json
{
  "title": "<string>",                    // Level title
  "description": "<string>",              // Problem description (supports \n for newlines)
  "input_type": "<string>",               // "text" or "number" (HTML input type)
  "placeholder": "<string>",              // Input field placeholder
  "expected_answer": "<string>"           // Correct answer (ALWAYS a string, even for numbers)
}
```

**Optional Fields**:
```json
{
  "input_file": "<string>",  // Filename of input file in same level folder
  "hint": "<string>"         // Optional hint to help solve the exercise
}
```

**Important Notes**:
- `expected_answer` must be a **string**: `"42"` not `42`, `"Hello"` not `"hello"`
- Use `{{input}}` placeholder in description when using input_file
- The `{{input}}` will be replaced with file content
- `input_type` must be exactly `"text"` or `"number"`

---

## Summary.md File

**Location**: `competitions/{folder-name}/Summary.md`

The Summary.md file provides structured information about the competition that can be read by both humans and the AI competition engine. This file helps participants understand the competition structure and assists the AI in providing contextual help.

### Required Sections

The Summary.md file MUST include these sections with these exact headers (using ## for markdown headers):

#### 1. Overview
**Header**: `## Overview`
**Content**: Brief 2-3 sentence description of the competition theme and objectives

**Example**:
```markdown
## Overview

This competition explores prime number theory through progressively challenging problems. Participants will learn to detect primes, generate prime sequences, and apply prime concepts to real-world scenarios like cryptography and factorization.
```

#### 2. Story
**Header**: `## Story`
**Content**: 1-2 paragraph narrative that sets the context and theme for the competition. Should explain WHY participants are solving these problems and provide engaging context.

**Example**:
```markdown
## Story

You've joined a Swedish Arctic research station in Kiruna, studying the mathematical patterns found in snowflake formations. The lab director needs your help analyzing sensor data and predicting snowflake patterns based on atmospheric conditions. Each level takes you deeper into the world of crystallography and pattern analysis, from basic symmetry detection to complex predictive modeling using IoT sensor networks.
```

#### 3. Level Progression
**Header**: `## Level Progression`
**Content**: Structured breakdown of each level showing the learning path. Use markdown subheaders for each level.

**Format**:
```markdown
## Level Progression

### Level 1: [Title]
**Concept**: [What concept is being taught]
**Task**: [What the participant needs to do]
**Skills**: [Specific programming/algorithmic skills needed]

### Level 2: [Title]
**Concept**: [What concept is being taught]
**Task**: [What the participant needs to do]
**Skills**: [Specific programming/algorithmic skills needed]

[... continue for all levels ...]
```

**Example**:
```markdown
## Level Progression

### Level 1: Symmetry Detection
**Concept**: Basic pattern recognition
**Task**: Determine if a snowflake pattern is perfectly symmetric
**Skills**: String operations, set theory, basic comparison

### Level 2: Storm Analysis
**Concept**: Iteration and filtering
**Task**: Count symmetric snowflakes in a dataset
**Skills**: File parsing, loops, conditional filtering
```

#### 4. Learning Objectives
**Header**: `## Learning Objectives`
**Content**: Bullet list of key skills and concepts participants will master

**Example**:
```markdown
## Learning Objectives

- String manipulation and pattern analysis
- Working with multiple data formats (CSV, JSON, text files)
- Statistical analysis and filtering
- Rule-based decision systems
- IoT sensor data interpretation
```

### Optional Sections

These sections are recommended but not required:

#### Difficulty Curve
**Header**: `## Difficulty Curve`
**Content**: Visual representation of difficulty progression

**Example**:
```markdown
## Difficulty Curve

- Level 1: ⭐ Easy - Introduction to concepts
- Level 2: ⭐⭐ Medium - Apply concepts iteratively
- Level 3: ⭐⭐⭐ Challenging - New algorithmic thinking
- Level 4: ⭐⭐⭐⭐ Advanced - Complex data structures
- Level 5: ⭐⭐⭐⭐⭐ Expert - Synthesis of all concepts
```

#### Context
**Header**: `## Context`
**Content**: Domain-specific information that makes the competition authentic (e.g., real locations, technical background, industry relevance)

**Example**:
```markdown
## Context

This competition uses real atmospheric data patterns from Kiruna, Sweden (67.8558°N), one of Europe's northernmost research stations. The sensor network and data formats mirror actual IoT deployments in Nordic smart infrastructure projects.
```

#### Estimated Time
**Header**: `## Estimated Time`
**Content**: Expected completion time and breakdown

**Example**:
```markdown
## Estimated Time

**Total**: 45-60 minutes
- Levels 1-2: 10-15 minutes (fundamentals)
- Level 3: 15-20 minutes (algorithm development)
- Levels 4-5: 20-25 minutes (advanced analysis)
```

### Summary.md Template

```markdown
# [Competition Name]

## Overview

[2-3 sentences describing the competition theme and what participants will learn]

## Story

[1-2 paragraphs providing engaging context and explaining why participants are solving these problems]

## Level Progression

### Level 1: [Title]
**Concept**: [Core concept]
**Task**: [What to do]
**Skills**: [Required skills]

### Level 2: [Title]
**Concept**: [Core concept]
**Task**: [What to do]
**Skills**: [Required skills]

[... continue for all levels ...]

## Learning Objectives

- [Skill/concept 1]
- [Skill/concept 2]
- [Skill/concept 3]
- [etc.]

## Difficulty Curve

- Level 1: ⭐ [Description]
- Level 2: ⭐⭐ [Description]
[... continue for all levels ...]

## Context

[Optional: Domain-specific background, real-world connections, authenticity details]

## Estimated Time

**Total**: [X] minutes
[Optional: breakdown by level or section]
```

### AI Engine Integration

The AI competition engine will parse Summary.md to:
1. **Provide contextual help**: Understanding the story helps the AI give better hints
2. **Track progress**: Level progression helps track where participants are
3. **Suggest next steps**: Learning objectives guide the AI in recommending approaches
4. **Set expectations**: Difficulty curve and time estimates help manage participant expectations

### Validation Rules for Summary.md

- ✅ File named exactly `Summary.md` (capital S, lowercase ummary)
- ✅ Located in competition root directory (same level as config.json)
- ✅ Contains all 4 required sections with exact header names
- ✅ Uses markdown formatting (## for headers, ### for subheaders)
- ✅ Level Progression section covers ALL levels in the competition
- ✅ Each level in progression has Concept, Task, and Skills fields

---

## Examples

### Example 1: Simple Level (No Input File)

**config.json**:
```json
{
  "title": "Level 1: Count Vowels",
  "description": "Count the number of vowels (a, e, i, o, u) in: 'Programming is fun!'",
  "input_type": "number",
  "placeholder": "Enter the number of vowels",
  "expected_answer": "5"
}
```

### Example 2: Level with Input File

**config.json**:
```json
{
  "title": "Level 2: Sum Numbers",
  "description": "Sum all numbers in this file:\n\n{{input}}",
  "input_type": "number",
  "placeholder": "Enter the sum",
  "expected_answer": "273",
  "input_file": "input.txt"
}
```

**input.txt** (in same folder):
```
10
20
30
40
50
```

### Example 3: Text Input with File

**config.json**:
```json
{
  "title": "Level 3: Decrypt Message",
  "description": "Decrypt this Caesar cipher (shift 7): '{{input}}'",
  "input_type": "text",
  "placeholder": "Enter decrypted text",
  "expected_answer": "Hello, World!",
  "input_file": "secret.txt"
}
```

### Example 4: Level with Hint

**config.json**:
```json
{
  "title": "Level 1: Count Vowels",
  "description": "Count the number of vowels (a, e, i, o, u) in: 'Programming is fun!'",
  "input_type": "number",
  "placeholder": "Enter the number of vowels",
  "expected_answer": "5",
  "hint": "Räkna noggrant alla vokaler, både stora och små bokstäver."
}
```

---

## Input File Format Examples

The system supports various input file formats. Here are examples for different data types:

### CSV Files

**config.json**:
```json
{
  "title": "Sales Data Analysis",
  "description": "Calculate the total sales from this CSV file:\n\n{{input}}\n\nWhat is the sum of all sales amounts?",
  "input_type": "number",
  "placeholder": "Enter total sales",
  "expected_answer": "15750",
  "input_file": "sales.csv"
}
```

**sales.csv**:
```csv
date,product,amount
2024-01-01,Widget A,5000
2024-01-02,Widget B,3250
2024-01-03,Widget A,7500
```

**solution.py**:
```python
import csv

total = 0
with open('sales.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += int(row['amount'])

print(total)
```

### JSON Files

**config.json**:
```json
{
  "title": "API Response Parser",
  "description": "Parse this JSON API response:\n\n{{input}}\n\nHow many users have admin privileges?",
  "input_type": "number",
  "placeholder": "Enter count",
  "expected_answer": "2",
  "input_file": "users.json"
}
```

**users.json**:
```json
{
  "users": [
    {"name": "Alice", "role": "admin"},
    {"name": "Bob", "role": "user"},
    {"name": "Charlie", "role": "admin"},
    {"name": "Diana", "role": "user"}
  ]
}
```

**solution.py**:
```python
import json

with open('users.json', 'r') as f:
    data = json.load(f)

admin_count = sum(1 for user in data['users'] if user['role'] == 'admin')
print(admin_count)
```

### Log Files

**config.json**:
```json
{
  "title": "Error Log Analysis",
  "description": "Analyze this server log:\n\n{{input}}\n\nHow many ERROR level entries are there?",
  "input_type": "number",
  "placeholder": "Enter error count",
  "expected_answer": "3",
  "input_file": "server.log"
}
```

**server.log**:
```
2024-11-06 10:00:00 INFO Server started
2024-11-06 10:05:23 ERROR Connection timeout
2024-11-06 10:10:45 WARNING High memory usage
2024-11-06 10:15:12 ERROR Database connection failed
2024-11-06 10:20:33 INFO Request processed
2024-11-06 10:25:01 ERROR Authentication failed
```

**solution.py**:
```python
with open('server.log', 'r') as f:
    lines = f.readlines()

error_count = sum(1 for line in lines if 'ERROR' in line)
print(error_count)
```

### Binary/Hex Data

**config.json**:
```json
{
  "title": "CAN Bus Message Parser",
  "description": "Parse this CAN bus log:\n\n{{input}}\n\nWhat is the highest message ID (in decimal)?",
  "input_type": "number",
  "placeholder": "Enter highest ID",
  "expected_answer": "512",
  "input_file": "canbus.log"
}
```

**canbus.log**:
```
ID: 0x100 Data: 01 23 45 67
ID: 0x200 Data: 89 AB CD EF
ID: 0x150 Data: 11 22 33 44
```

**solution.py**:
```python
import re

max_id = 0
with open('canbus.log', 'r') as f:
    for line in f:
        match = re.search(r'ID: (0x[0-9A-Fa-f]+)', line)
        if match:
            id_value = int(match.group(1), 16)
            max_id = max(max_id, id_value)

print(max_id)
```

### Multi-line Text Files

**config.json**:
```json
{
  "title": "Network Configuration",
  "description": "Parse this network config:\n\n{{input}}\n\nHow many servers are configured with port 443?",
  "input_type": "number",
  "placeholder": "Enter count",
  "expected_answer": "2",
  "input_file": "network.conf"
}
```

**network.conf**:
```
server {
  host: 192.168.1.10
  port: 443
}

server {
  host: 192.168.1.11
  port: 80
}

server {
  host: 192.168.1.12
  port: 443
}
```

**solution.py**:
```python
with open('network.conf', 'r') as f:
    content = f.read()

# Count occurrences of "port: 443"
count = content.count('port: 443')
print(count)
```

---

## Theme and Story Integration

Creating a cohesive theme makes competitions more engaging and memorable. A good theme ties levels together and provides context for why participants are solving these problems.

### Elements of Good Competition Themes

1. **Overarching Narrative**: A story or concept that connects all levels
2. **Progressive Journey**: Each level advances the story or deepens the theme
3. **Contextual Problems**: Challenges make sense within the theme
4. **Consistent Terminology**: Use theme-specific language throughout

### Theme Examples

**Mathematical Journey**
- "Prime Odyssey" - exploring prime numbers from detection to cryptography
- "Fibonacci Quest" - unraveling the mysteries of the golden ratio
- "Matrix Mysteries" - adventures in linear algebra

**Real-World Scenarios**
- "Smart City Challenge" - IoT sensor networks and urban optimization
- "Autonomous Vehicle Academy" - CAN bus parsing to path planning
- "Nordic Weather Station" - analyzing climate data across Scandinavia

**Tech Domain Themes**
- "API Detective" - parsing and analyzing REST API responses
- "Log File Forensics" - investigating system logs for security issues
- "Database Expedition" - SQL queries from basic to complex

### Theme Structure Template

```
Competition Name: [Engaging Title]
Story Hook: [1-2 sentence setup]

Level 1: Introduction - [Basic concept in theme context]
Level 2: Building Skills - [Extend the concept]
Level 3: Challenge - [Apply skills in new way]
Level 4: Advanced Application - [Complex real-world scenario]
Level 5: Mastery - [Synthesis of all previous concepts]
```

### Example: "Arctic Data Center" Theme

**Competition Description**: 
"You're managing a data center in northern Sweden. Help optimize its operations through data analysis and algorithm design."

- **Level 1**: "Temperature Monitoring" - Parse sensor data to find average temperature
- **Level 2**: "Power Efficiency" - Calculate optimal cooling based on server load
- **Level 3**: "Network Traffic" - Analyze packet logs to find peak usage times
- **Level 4**: "Cost Optimization" - Balance power usage with renewable energy availability
- **Level 5**: "Predictive Maintenance" - Use historical data to predict equipment failures

---

## Difficulty Progression Guidelines

Properly scaling difficulty ensures participants stay engaged without becoming frustrated or bored.

### Progression Principles

1. **Start Accessible**: Level 1 should be solvable by most participants
2. **Incremental Complexity**: Each level should feel achievable if you solved the previous one
3. **Reuse Concepts**: Later levels build on earlier solutions
4. **Introduce One New Concept Per Level**: Don't overwhelm with multiple new ideas

### Difficulty Dimensions

You can increase difficulty along several axes:

**Input Complexity**
- Level 1: Single number
- Level 2: Small list (10-20 items)
- Level 3: Larger dataset (100s of items)
- Level 4: Complex structured data (nested JSON, CSV with multiple columns)
- Level 5: Real-world messy data requiring parsing/cleaning

**Algorithm Complexity**
- Level 1: Direct calculation (O(1) or O(n))
- Level 2: Simple iteration with one loop
- Level 3: Nested loops or basic recursion
- Level 4: Requires data structures (hash maps, sets)
- Level 5: Advanced algorithms (dynamic programming, graph algorithms)

**Problem Clarity**
- Level 1: Explicitly stated steps
- Level 2: Clear goal, obvious approach
- Level 3: Multiple valid approaches
- Level 4: Requires insight or pattern recognition
- Level 5: Ambiguous requirements requiring interpretation

### Example Progression: String Processing

**Level 1: Character Count**
- Input: Single word ("hello")
- Task: Count total characters
- Skill: Basic string operations
- Complexity: O(1) using len()

**Level 2: Vowel Count**
- Input: Sentence
- Task: Count vowels
- Skill: Iteration + conditionals
- Complexity: O(n) single pass

**Level 3: Word Frequency**
- Input: Paragraph
- Task: Find most common word
- Skill: String splitting + dictionary
- Complexity: O(n) with hash map

**Level 4: Anagram Detection**
- Input: List of words
- Task: Group anagrams together
- Skill: Sorting + grouping
- Complexity: O(n * m log m) where m is word length

**Level 5: Pattern Matching**
- Input: Text file + regex pattern
- Task: Extract and analyze matched patterns
- Skill: Regular expressions + data analysis
- Complexity: O(n) but requires regex knowledge

### Time Complexity Guidelines

- **Level 1-2**: O(1), O(n) - Simple iterations
- **Level 3**: O(n log n) - Sorting, basic searching
- **Level 4**: O(n²) acceptable - Nested loops for small inputs
- **Level 5**: May require optimization - Encourage efficient solutions

### Testing Your Progression

Before finalizing, ask:
1. Can each level be solved using skills from previous levels?
2. Does each level introduce exactly one new concept?
3. Would the difficulty curve frustrate or bore participants?
4. Do input sizes scale reasonably with complexity?

---

## Writing Effective Hints

Hints should guide without giving away the solution. Good hints help stuck participants make progress while preserving the learning experience.

### Hint Writing Principles

1. **Progressive Disclosure**: Start general, get more specific if needed
2. **Direct Attention**: Point to relevant concepts without solving
3. **Example-Based**: Show a similar but simpler problem
4. **Avoid Spoilers**: Never include code or exact answers
5. **Language Considerations**: Support multiple languages if needed

### Good vs Bad Hints

**❌ Bad Hint** (Too Specific):
```json
"hint": "Use a for loop from 2 to sqrt(n) and check if n % i == 0"
```

**✅ Good Hint** (Guides Thinking):
```json
"hint": "You only need to check divisors up to the square root of the number. Why might this be true?"
```

---

**❌ Bad Hint** (Gives Away Answer):
```json
"hint": "The answer is 42. Just calculate 2 + 3 + 5 + 7 + 11 + 14"
```

**✅ Good Hint** (Points Direction):
```json
"hint": "Break the number into its prime factors first, then think about what mathematical operation you need to perform on those factors."
```

---

**❌ Bad Hint** (Too Vague):
```json
"hint": "Think about it carefully and you'll figure it out."
```

**✅ Good Hint** (Actionable Guidance):
```json
"hint": "Start by identifying what makes two primes 'twins'. Then, generate all primes in the range and look for this pattern."
```

### Hint Templates

**For Algorithm Problems**:
```
"Think about [key concept]. You might find it helpful to [suggested approach] before [main task]."
```

**For Pattern Recognition**:
```
"Look carefully at [specific aspect]. Do you notice [type of pattern]?"
```

**For Optimization**:
```
"Your first approach might be [simple method], but can you find a way to [optimization goal] by [technique hint]?"
```

**For Data Structure Problems**:
```
"This problem becomes simpler if you use a [data structure type] to [benefit of using it]."
```

### Multi-Language Hints

If your competition serves an international audience, consider hints in multiple languages:

```json
{
  "hint": "Try dividing the number by all integers from 2 up to the square root. If any divide evenly, it's not prime.",
  "hint_sv": "Prova att dela talet med alla heltal från 2 upp till kvadratroten. Om något delar jämnt är det inte ett primtal.",
  "hint_no": "Prøv å dele tallet med alle heltall fra 2 opp til kvadratroten. Hvis noen deler jevnt, er det ikke et primtall."
}
```

### When to Include Hints

- **Always for Level 1**: Help participants get started
- **For Complex Levels**: When introducing new concepts or algorithms
- **For Ambiguous Problems**: When requirements might be misunderstood
- **Skip for Mid-Levels**: Let participants build confidence independently

---

## Common Problem Patterns Library

Pre-built competition structures you can adapt for different domains. Each pattern includes a complete 5-level progression.

### Pattern 1: Detection → Counting → Generation → Analysis → Optimization

**Example: Prime Numbers**
1. Is it prime? (single number)
2. Count primes (in a range)
3. Generate the Nth prime
4. Prime factorization
5. Twin primes / prime gaps

**Example: Palindromes**
1. Is it a palindrome?
2. Count palindromes in a list
3. Generate palindromic numbers
4. Longest palindrome substring
5. Palindrome permutations

### Pattern 2: Parse → Filter → Transform → Aggregate → Predict

**Example: Log File Analysis**
1. Parse single log entry
2. Filter by severity level
3. Transform timestamps to local time
4. Aggregate error statistics
5. Predict next failure time

**Example: Sensor Data**
1. Read single sensor value
2. Filter out invalid readings
3. Convert units (Celsius to Fahrenheit)
4. Calculate moving average
5. Detect anomalies

### Pattern 3: Search → Sort → Match → Combine → Optimize

**Example: Database Queries**
1. Find record by ID
2. Sort records by field
3. Match records across tables
4. Join multiple datasets
5. Query optimization

**Example: String Matching**
1. Find exact substring
2. Sort words alphabetically
3. Match patterns with wildcards
4. Combine and deduplicate results
5. Efficient pattern matching

### Pattern 4: Simulate → Calculate → Predict → Optimize → Scale

**Example: Network Simulation**
1. Simulate single packet transmission
2. Calculate total bandwidth
3. Predict congestion points
4. Optimize routing
5. Scale to large networks

### Nordic/Automotive/IoT Specific Patterns

### Pattern 5: CAN Bus Message Analysis

**Level 1: Message Parsing**
```json
{
  "title": "CAN Message Decoder",
  "description": "Parse this CAN bus message and extract the message ID:\n\n{{input}}",
  "input_file": "can_message.txt"
}
```
Content: `ID: 0x123 Data: 01 02 03 04 05 06 07 08`

**Level 2: Data Field Extraction**
Extract specific data fields from CAN messages (e.g., engine RPM from bytes 2-3)

**Level 3: Signal Conversion**
Convert raw CAN data to engineering units using scaling factors

**Level 4: Message Filtering**
Filter messages by ID range and calculate statistics

**Level 5: Bus Load Analysis**
Calculate CAN bus utilization and identify potential bottlenecks

### Pattern 6: Nordic Weather Data

**Level 1: Temperature Reading**
Parse temperature from weather station data

**Level 2: Daily Statistics**
Calculate min/max/average for the day

**Level 3: Trend Detection**
Identify warming or cooling trends over weeks

**Level 4: Regional Comparison**
Compare weather patterns across Stockholm, Oslo, Helsinki

**Level 5: Season Prediction**
Use historical data to predict seasonal transitions

### Pattern 7: IoT Sensor Network

**Level 1: Single Sensor Reading**
Parse JSON from one IoT sensor

**Level 2: Multi-Sensor Aggregation**
Combine data from multiple sensors in a room

**Level 3: Time-Series Analysis**
Analyze sensor readings over time

**Level 4: Anomaly Detection**
Identify faulty sensors or unusual readings

**Level 5: Network Optimization**
Determine optimal sensor placement for coverage

### Pattern 8: Electric Vehicle Charging

**Level 1: Battery State**
Calculate state of charge from voltage readings

**Level 2: Charging Time**
Estimate time to full charge at current rate

**Level 3: Optimal Charging**
Find cheapest charging time based on electricity prices

**Level 4: Load Balancing**
Distribute charging across multiple vehicles

**Level 5: Grid Integration**
Balance EV charging with renewable energy availability

### Pattern 9: Smart Building Automation

**Level 1: Occupancy Detection**
Determine if room is occupied from sensor data

**Level 2: HVAC Control**
Calculate optimal temperature settings

**Level 3: Energy Monitoring**
Track energy consumption by zone

**Level 4: Predictive Climate Control**
Pre-heat/cool based on schedule

**Level 5: Building-Wide Optimization**
Minimize energy while maintaining comfort

### Quick-Start Competition Templates

**Template: "Algorithm Fundamentals"**
- Focus: Core programming concepts
- Domains: Sorting, searching, recursion
- Difficulty: Beginner to intermediate
- Time: 30-60 minutes

**Template: "Data Structures Deep Dive"**
- Focus: Arrays, lists, maps, sets, trees
- Domains: Abstract data manipulation
- Difficulty: Intermediate
- Time: 60-90 minutes

**Template: "Real-World Applications"**
- Focus: Practical problem-solving
- Domains: Log parsing, data analysis, APIs
- Difficulty: Intermediate to advanced
- Time: 90-120 minutes

**Template: "Nordic Smart Mobility"**
- Focus: Automotive and IoT
- Domains: CAN bus, sensors, optimization
- Difficulty: Advanced
- Time: 2-3 hours

---

## Step-by-Step Creation Process

1. **Choose Competition Folder Name**: Use any descriptive name (e.g., `competition1`, `my-comp`, `external-2024`)
2. **Create Folder**: `competitions/{your-folder-name}/`
3. **Create Competition config.json** with UUID id, name, description
4. **Create Summary.md** with required sections (Overview, Story, Level Progression, Learning Objectives)
5. **Create Level Folder**: `level1/` inside competition folder
6. **Create Level config.json** with all required fields (title, description, input_type, placeholder, expected_answer)
7. **Add Optional Hint** (if desired): Add `"hint"` field to level config.json with helpful guidance
8. **Add Input File** (if needed): Place in level folder, reference in config
9. **Add solution.py** (optional): Reference solution for testing
10. **Repeat for Additional Levels**: level2/, level3/, etc.
11. **Update Summary.md Level Progression**: Add each new level to the Level Progression section
12. **Validate Structure**: Check all files exist, JSON is valid, UUID is present
13. **Create Zip File**: Package the entire competition folder as a zip file for download
14. **Automated Testing**: Run solution.py for each level and verify output matches expected_answer

---

## Automated Testing and Validation

Before finalizing a competition, always test that solutions produce the correct answers. This catches mathematical errors, typos in expected_answer, and logic bugs.

### Pre-Deployment Testing Process

**1. Test Each Solution Individually**
```bash
# Navigate to each level and run solution
cd competition-name/level1
python3 solution.py

# Verify output matches expected_answer in config.json
```

**2. Automated Validation Script**

Create a test script to validate all levels at once:

```python
#!/usr/bin/env python3
"""validate_competition.py - Test all levels in a competition"""

import json
import subprocess
import sys
from pathlib import Path

def validate_level(level_path):
    """Validate a single level."""
    config_path = level_path / "config.json"
    solution_path = level_path / "solution.py"
    
    # Check config exists
    if not config_path.exists():
        return False, f"Missing config.json in {level_path}"
    
    # Load expected answer
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    expected = config.get('expected_answer')
    if expected is None:
        return False, f"No expected_answer in {level_path}/config.json"
    
    # Run solution if it exists
    if solution_path.exists():
        try:
            result = subprocess.run(
                ['python3', 'solution.py'],
                cwd=level_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            actual = result.stdout.strip()
            
            if actual == expected:
                return True, f"✅ {level_path.name}: PASS"
            else:
                return False, f"❌ {level_path.name}: Expected '{expected}', got '{actual}'"
        
        except subprocess.TimeoutExpired:
            return False, f"❌ {level_path.name}: Timeout (>10s)"
        except Exception as e:
            return False, f"❌ {level_path.name}: Error - {e}"
    
    return True, f"⚠️  {level_path.name}: No solution.py to test"

def validate_competition(competition_path):
    """Validate all levels in a competition."""
    print(f"Validating competition: {competition_path.name}\n")
    
    # Find all level directories
    levels = sorted([d for d in competition_path.iterdir() 
                    if d.is_dir() and d.name.startswith('level')])
    
    if not levels:
        print("❌ No level directories found!")
        return False
    
    all_passed = True
    for level in levels:
        passed, message = validate_level(level)
        print(message)
        if not passed:
            all_passed = False
    
    print(f"\n{'='*50}")
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed - review output above")
    
    return all_passed

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 validate_competition.py <competition-directory>")
        sys.exit(1)
    
    comp_path = Path(sys.argv[1])
    if not comp_path.exists():
        print(f"Error: {comp_path} does not exist")
        sys.exit(1)
    
    success = validate_competition(comp_path)
    sys.exit(0 if success else 1)
```

**Usage:**
```bash
python3 validate_competition.py prime-odyssey/
```

**Example Output:**
```
Validating competition: prime-odyssey

✅ level1: PASS
✅ level2: PASS
✅ level3: PASS
✅ level4: PASS
✅ level5: PASS

==================================================
✅ All tests passed!
```

### Common Testing Issues

**Issue: Solution produces correct value but wrong type**
```python
# ❌ Wrong - returns integer
print(42)

# ✅ Correct - returns string
print("42")
```

**Issue: Extra whitespace in output**
```python
# ❌ Wrong - has trailing newline issues
print("answer\n")

# ✅ Correct - clean output
print("answer")
```

**Issue: Floating point precision**
```python
# ❌ Wrong - too many decimals
print(3.14159265359)

# ✅ Correct - matches expected format
print("3.14")
```

### Validation Checklist Before Deployment

Run through this checklist before creating the final zip file:

- [ ] All level directories follow `level{N}` naming (level1, level2, ...)
- [ ] Competition config.json has valid UUID, name, and description
- [ ] Summary.md file exists in competition root directory
- [ ] Summary.md contains all 4 required sections (Overview, Story, Level Progression, Learning Objectives)
- [ ] Summary.md Level Progression covers all levels in the competition
- [ ] Each level in Summary.md has Concept, Task, and Skills fields
- [ ] Each level has valid config.json with all required fields
- [ ] All `expected_answer` values are strings (not numbers or booleans)
- [ ] All referenced input files exist in their level directories
- [ ] File names in config.json exactly match actual file names (case-sensitive)
- [ ] All JSON files are valid (no trailing commas, proper quotes)
- [ ] Each solution.py (if present) runs without errors
- [ ] Each solution.py output matches expected_answer exactly
- [ ] Hints are present and helpful (especially for Level 1 and complex levels)
- [ ] Competition theme is cohesive across all levels
- [ ] Difficulty progression feels smooth and logical
- [ ] No extra directories (like `level{1..5}`) are present
- [ ] Input files contain appropriate test data
- [ ] Level descriptions are clear and unambiguous
- [ ] Tested the competition by extracting zip and loading in system

---

## Validation Rules

### Competition Validation
- ✅ Folder name: Any valid folder name (no strict pattern required)
- ✅ `config.json` exists and is valid JSON
- ✅ Has `id` (UUID string, auto-generated if missing), `name`, `description` fields
- ✅ `Summary.md` exists with all 4 required sections
- ✅ At least one level folder exists
- ✅ Zip file created containing complete competition structure (competition folder, config.json, Summary.md, all levels, config files, input files, solution files)

### Level Validation
- ✅ Folder name: `level{N}` format, starting at 1
- ✅ `config.json` exists and is valid JSON
- ✅ Has all required fields: `title`, `description`, `input_type`, `placeholder`, `expected_answer`
- ✅ `input_type` is `"text"` or `"number"`
- ✅ `expected_answer` is a string
- ✅ If `input_file` specified, file exists in level folder
- ✅ If `hint` specified, it's a string providing helpful guidance

### JSON Validation
- ✅ Valid JSON syntax (no trailing commas, proper quotes)
- ✅ All strings use double quotes `"`
- ✅ Proper escaping of special characters

---

## Directory Creation Best Practices

### CRITICAL: Avoid Brace Expansion Issues

When creating multiple level directories, **NEVER** use brace expansion like this:
```bash
# ❌ WRONG - This can create a literal "level{1..5}" directory
mkdir -p competition-name/level{1..5}
```

Instead, **ALWAYS** create directories individually or use a proper loop:

**Method 1: Create directories individually (RECOMMENDED)**
```bash
# ✅ CORRECT - Create each directory explicitly
mkdir -p competition-name/level1
mkdir -p competition-name/level2
mkdir -p competition-name/level3
mkdir -p competition-name/level4
mkdir -p competition-name/level5
```

**Method 2: Use a for loop**
```bash
# ✅ CORRECT - Use a loop to create directories
cd competition-name
for i in 1 2 3 4 5; do mkdir -p level$i; done
```

**Why this matters**: Some bash environments may interpret `{1..5}` as a literal string in addition to expanding it, creating an unwanted `level{1..5}` directory that will break the competition import process.

---

## Common Issues & Solutions

### Extra "level{1..5}" Directory Created
- **Issue**: A literal `level{1..5}` directory appears alongside level1, level2, etc.
- **Cause**: Using brace expansion `mkdir level{1..5}` in certain bash contexts
- **Solution**: Delete the extra directory and recreate using individual mkdir commands or a for loop
- **Prevention**: Always create level directories individually, never use brace expansion

### Competition Not Loading
- **Issue**: Invalid JSON syntax
- **Solution**: Validate JSON, check for trailing commas, ensure all strings use double quotes

### Level Not Appearing
- **Issue**: Wrong folder name format
- **Solution**: Must be `level1`, `level2`, etc. (lowercase, no hyphens/underscores)

### Input File Not Downloading
- **Issue**: Filename mismatch
- **Solution**: Check exact filename in `config.json` matches actual file (case-sensitive)

### Answer Not Accepted
- **Issue**: `expected_answer` format wrong
- **Solution**: Must be string (`"42"` not `42`), exact match required (case/whitespace sensitive)

---

## When User Asks to Create a Competition

1. **Gather Requirements**:
   - Competition name and description
   - Number of levels
   - Problem descriptions for each level
   - Whether input files are needed
   - Expected answers

2. **Determine Competition Number**:
   - Ask user or help them check existing competitions
   - Suggest next available number

3. **Generate Files**:
   - Create competition `config.json` with UUID
   - Create level folders and `config.json` for each (include optional `hint` field if desired)
   - If input files needed, provide example structure
   - Optionally generate `solution.py` templates
   - Create zip file containing the entire competition structure

4. **Provide Validation**:
   - Check all naming conventions
   - Verify JSON syntax
   - Confirm all required fields present

5. **Give Testing Instructions**:
   - Explain how to test (restart server)
   - What to check in server logs
   - How to verify in web interface

---

## Response Templates

### When User Asks "How do I create a competition?"

Start with: "I'll help you create a competition directory. First, I need:
1. Competition name and description
2. How many levels?
3. Brief description of each level's problem
4. Any input files needed?

Once I have this, I'll generate all the config.json files and folder structure for you, and create a zip file ready for download."

### When Generating config.json

Always provide:
- Complete, valid JSON
- All required fields
- Proper formatting
- Comments explaining choices (if helpful)

### When Validating User's Structure

Check and report:
- Folder naming: ✅ or ❌ with specific issue
- JSON validity: ✅ or ❌ with error details
- Required fields: ✅ or ❌ listing missing fields
- File references: ✅ or ❌ noting missing files

---

## Best Practices to Recommend

1. **Include UUID** in competition config.json for proper tracking
2. **Create Summary.md** with all required sections for AI engine integration
3. **Use sequential level numbers** (level1, level2, level3)
4. **Always create solution.py** for testing and validation
5. **Test expected_answer** matches solution output exactly before deployment
6. **Use descriptive filenames** for input files that indicate content
7. **Add helpful hints** to level configs, especially for Level 1 and complex problems
8. **Validate JSON** before deploying (use a JSON validator)
9. **Create zip file** containing complete competition structure for easy distribution
10. **Start simple** - verify first level works before adding more
11. **Progressive difficulty** - each level should build on previous ones
12. **Choose a cohesive theme** - tie levels together with a narrative or domain
13. **Provide diverse input formats** - use CSV, JSON, logs as appropriate for realism
14. **Write guiding hints** - help without spoiling the solution
15. **Test all solutions** - run automated validation before finalizing
16. **Consider time complexity** - ensure solutions can run within reasonable time limits
17. **Use realistic data** - especially for domain-specific competitions (automotive, IoT, etc.)
18. **Clear level descriptions** - be explicit about what participants need to do
19. **Consistent terminology** - use the same terms throughout the competition
20. **Review difficulty curve** - ensure smooth progression without sudden difficulty spikes
21. **Clean directory structure** - remove any extra/temporary files before zipping
22. **Update Summary.md as you add levels** - keep Level Progression section synchronized

---

## Quick Reference

| Element | Format | Example |
|---------|--------|---------|
| Competition folder | Any folder name | `competition4`, `my-comp`, `external-2024` |
| Competition ID | UUID string | `"1029bb53-31e5-4e35-8d13-b0da3e20091b"` |
| Level folder | `level{N}` | `level1` |
| Competition config | `config.json` | `{id (UUID), name, description}` |
| Level config | `config.json` | `{title, description, input_type, placeholder, expected_answer, hint (optional)}` |
| Input type | `"text"` or `"number"` | `"number"` |
| Expected answer | Always string | `"42"` |
| Input file | Any filename | `input.txt` |

---

## Special Instructions

- **Always validate JSON** before showing it to users
- **Use descriptive folder names** - any valid folder name is allowed
- **Include UUID in config.json** - recommended for consistency (will be auto-generated if missing)
- **ALWAYS create Summary.md** - required file with Overview, Story, Level Progression, and Learning Objectives sections
- **Competition IDs are UUIDs** - not integers, stored as strings in config.json
- **Double-check string quotes** - must be double quotes `"`
- **Verify expected_answer format** - must be string representation
- **Include hints when helpful** - see "Writing Effective Hints" section for guidance
- **Create zip files** - competitions should be packaged as zip files for easy download and deployment
- **Choose appropriate input formats** - see "Input File Format Examples" for CSV, JSON, logs, etc.
- **Design cohesive themes** - see "Theme and Story Integration" section
- **Plan difficulty progression** - see "Difficulty Progression Guidelines" section
- **Use problem patterns** - see "Common Problem Patterns Library" for templates
- **Test before deploying** - see "Automated Testing and Validation" section
- **Provide complete examples** - show full file structures
- **Guide step-by-step** - don't overwhelm with all info at once
- **CRITICAL: Create level directories individually** - NEVER use bash brace expansion like `mkdir level{1..5}` as this can create a literal `level{1..5}` directory which will break imports. Always create directories one at a time or use a loop

---

## Zip File Creation

When creating a competition, you should provide the complete competition structure as a **zip file** that users can download and deploy. The zip file should contain:

- The competition folder (e.g., `competition1/`, `my-comp/`, etc.)
- Competition `config.json` with UUID
- **`Summary.md` with all required sections**
- All level folders (`level1/`, `level2/`, etc.)
- Each level's `config.json` file
- All input files referenced in level configs
- All `solution.py` files (if present)

**Zip File Structure Example**:
```
competition1.zip
└── competition1/
    ├── config.json
    ├── Summary.md
    ├── level1/
    │   ├── config.json
    │   ├── solution.py (optional)
    │   └── input.txt (optional)
    └── level2/
        ├── config.json
        └── solution.py (optional)
```

**Instructions for Users**:
1. Download the zip file
2. Extract it to the `competitions/` directory
3. Restart the server to load the competition
4. The competition will be automatically discovered and registered

## Remember

- The system auto-discovers competitions - no code changes needed
- Competitions load on server startup
- Database registration happens automatically
- Validation is strict (exact string matching for answers)
- JSON syntax must be perfect (trailing commas will break it)
- Include UUID in competition config.json - each competition should have a UUID
- Create zip files - competitions should be packaged as downloadable zip files

Use this skill to help users create competition directories with confidence and accuracy.


