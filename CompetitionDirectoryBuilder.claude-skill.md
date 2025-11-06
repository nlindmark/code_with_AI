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

## Step-by-Step Creation Process

1. **Choose Competition Folder Name**: Use any descriptive name (e.g., `competition1`, `my-comp`, `external-2024`)
2. **Create Folder**: `competitions/{your-folder-name}/`
3. **Create Competition config.json** with UUID id, name, description
4. **Create Level Folder**: `level1/` inside competition folder
5. **Create Level config.json** with all required fields (title, description, input_type, placeholder, expected_answer)
6. **Add Optional Hint** (if desired): Add `"hint"` field to level config.json with helpful guidance
7. **Add Input File** (if needed): Place in level folder, reference in config
8. **Add solution.py** (optional): Reference solution for testing
9. **Repeat for Additional Levels**: level2/, level3/, etc.
10. **Validate Structure**: Check all files exist, JSON is valid, UUID is present
11. **Create Zip File**: Package the entire competition folder as a zip file for download
12. **Test**: Restart server, verify competition loads (or extract zip and test)

---

## Validation Rules

### Competition Validation
- ✅ Folder name: Any valid folder name (no strict pattern required)
- ✅ `config.json` exists and is valid JSON
- ✅ Has `id` (UUID string, auto-generated if missing), `name`, `description` fields
- ✅ At least one level folder exists
- ✅ Zip file created containing complete competition structure (competition folder, all levels, config files, input files, solution files)

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

## Common Issues & Solutions

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
2. **Use sequential level numbers** (level1, level2, level3)
3. **Always create solution.py** for testing
4. **Test expected_answer** matches solution output exactly
5. **Use descriptive filenames** for input files
6. **Add helpful hints** to level configs when appropriate
7. **Validate JSON** before deploying
8. **Create zip file** containing complete competition structure for easy distribution
9. **Start simple** - verify first level works before adding more
10. **Progressive difficulty** - easier problems in earlier levels

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
- **Competition IDs are UUIDs** - not integers, stored as strings in config.json
- **Double-check string quotes** - must be double quotes `"`
- **Verify expected_answer format** - must be string representation
- **Include hints when helpful** - optional `hint` field can provide guidance to users
- **Create zip files** - competitions should be packaged as zip files for easy download and deployment
- **Provide complete examples** - show full file structures
- **Guide step-by-step** - don't overwhelm with all info at once

---

## Zip File Creation

When creating a competition, you should provide the complete competition structure as a **zip file** that users can download and deploy. The zip file should contain:

- The competition folder (e.g., `competition1/`, `my-comp/`, etc.)
- Competition `config.json` with UUID
- All level folders (`level1/`, `level2/`, etc.)
- Each level's `config.json` file
- All input files referenced in level configs
- All `solution.py` files (if present)

**Zip File Structure Example**:
```
competition1.zip
└── competition1/
    ├── config.json
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


