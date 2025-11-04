# Competition Directory Builder - Quick Reference Card

## For Claude: Quick Decision Tree

When helping users create competitions, use this quick reference:

### 1. Structure Check
```
competitions/
└── competition{N}/
    ├── config.json          ✓ Required
    └── level{M}/
        ├── config.json      ✓ Required
        ├── solution.py      ○ Optional
        └── {file}           ○ Optional (if referenced)
```

### 2. Naming Validation
- ✅ `competition4` → Valid
- ✅ `level1` → Valid  
- ❌ `competition-4` → Invalid (no hyphens)
- ❌ `Level1` → Invalid (must be lowercase)

### 3. Competition config.json
```json
{
  "id": 4,
  "name": "Competition Name",
  "description": "Description"
}
```

### 4. Level config.json (Minimum)
```json
{
  "title": "Level Title",
  "description": "Problem description",
  "input_type": "number",
  "placeholder": "Enter answer",
  "expected_answer": "42"
}
```

### 5. Critical Rules
- `expected_answer` ALWAYS string: `"42"` not `42`
- `input_type` exactly `"text"` or `"number"`
- JSON: double quotes only, no trailing commas
- File references: exact match (case-sensitive)

### 6. Common Mistakes
- ❌ Trailing comma: `"expected_answer": "42",`
- ❌ Wrong type: `"expected_answer": 42`
- ❌ Wrong folder: `competition-4` or `Level1`
- ❌ Missing quotes: `"expected_answer": hello`

### 7. Validation Checklist
1. Folder name: `competition{N}`?
2. Level folder: `level{N}` starting at 1?
3. JSON valid? (use validator)
4. All required fields present?
5. `expected_answer` is string?
6. Input file exists if referenced?
7. No trailing commas?

### 8. Response Flow
1. Ask: Name, levels, problems, files?
2. Determine: Next competition number
3. Generate: All config.json files
4. Validate: Check all rules
5. Provide: Testing instructions

---

Use this quick reference during conversations to ensure accuracy and consistency.


