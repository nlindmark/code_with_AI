"""
Competition loader - dynamically loads competitions from folder structure.

Scans the competitions/ directory and loads all competition configurations.
Supports UUID-based competition IDs and any folder name.
"""
import os
import json
import uuid
import re
from pathlib import Path
from typing import Dict, Any, Optional


def load_competitions(competitions_dir: str = "competitions") -> Dict[str, Dict[str, Any]]:
    """
    Loads all competitions from the competitions directory.
    
    Args:
        competitions_dir: Path to competitions directory
        
    Returns:
        Dictionary mapping competition UUIDs (strings) to competition data
    """
    competitions = {}
    competitions_path = Path(competitions_dir)
    
    if not competitions_path.exists():
        print(f"⚠️  Warning: Competitions directory '{competitions_dir}' not found")
        return competitions
    
    # Scan for competition folders (any folder name)
    for item in competitions_path.iterdir():
        if not item.is_dir():
            continue
        
        # Skip hidden directories
        if item.name.startswith('.'):
            continue
        
        # Load competition config
        comp_config_path = item / "config.json"
        if not comp_config_path.exists():
            print(f"⚠️  Warning: No config.json found in '{item.name}', skipping")
            continue
        
        try:
            with open(comp_config_path, 'r', encoding='utf-8') as f:
                comp_config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Invalid JSON in '{comp_config_path}': {e}")
            continue
        except Exception as e:
            print(f"⚠️  Warning: Error reading '{comp_config_path}': {e}")
            continue
        
        # Get or generate UUID
        comp_id = comp_config.get("id")
        if comp_id is None:
            # Generate UUID if not present
            comp_id = str(uuid.uuid4())
            print(f"⚠️  Warning: No 'id' field in '{comp_config_path}', generated UUID: {comp_id}")
        else:
            # Ensure ID is a string (UUID)
            comp_id = str(comp_id)
        
        # Validate UUID format
        try:
            uuid.UUID(comp_id)
        except ValueError:
            print(f"⚠️  Warning: Invalid UUID format '{comp_id}' in '{comp_config_path}', skipping")
            continue
        
        # Load Summary.md if it exists
        summary_data = _load_summary_md(item)
        
        # Build competition structure
        competition = {
            "name": comp_config.get("name", f"Competition {comp_id[:8]}"),
            "description": comp_config.get("description", ""),
            "folder_name": item.name,  # Store folder name for file path construction
            "summary": summary_data,  # Store parsed Summary.md content
            "levels": {}
        }
        
        # Load levels from level folders (level1, level2, etc.)
        for level_item in sorted(item.iterdir()):
            if not level_item.is_dir():
                continue
            
            if not level_item.name.startswith("level"):
                continue
            
            try:
                # Extract level number from folder name (level1 -> 1)
                level_id_str = level_item.name.replace("level", "")
                level_id = int(level_id_str)
            except ValueError:
                print(f"⚠️  Warning: Could not parse level ID from folder '{level_item.name}' in competition {comp_id[:8]}")
                continue
            
            # Load level config
            level_config_path = level_item / "config.json"
            if not level_config_path.exists():
                print(f"⚠️  Warning: No config.json found in '{level_item.name}', skipping")
                continue
            
            try:
                with open(level_config_path, 'r', encoding='utf-8') as f:
                    level_config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"⚠️  Warning: Invalid JSON in '{level_config_path}': {e}")
                continue
            except Exception as e:
                print(f"⚠️  Warning: Error reading '{level_config_path}': {e}")
                continue
            
            # Build level structure
            level = {
                "title": level_config.get("title", f"Level {level_id}"),
                "description": level_config.get("description", ""),
                "input_type": level_config.get("input_type", "text"),
                "placeholder": level_config.get("placeholder", ""),
                "expected_answer": level_config.get("expected_answer", "")
            }
            
            # Handle optional hint field
            hint = level_config.get("hint")
            if hint:
                level["hint"] = hint
            
            # Handle input file if specified - store filename for download, don't embed content
            input_file = level_config.get("input_file")
            if input_file:
                input_file_path = level_item / input_file
                if input_file_path.exists():
                    # Store input_file info for download functionality
                    level["input_file"] = input_file
                    # Remove {{input}} placeholder from description if present
                    if "{{input}}" in level["description"]:
                        level["description"] = level["description"].replace("{{input}}", "")
                        # Clean up any extra whitespace/newlines
                        level["description"] = level["description"].strip()
                else:
                    print(f"⚠️  Warning: Input file '{input_file_path}' not found for level {level_id} in competition {comp_id[:8]}")
            
            # Check for solution.py file
            solution_file = level_item / "solution.py"
            if solution_file.exists():
                level["solution_file"] = "solution.py"
            
            competition["levels"][level_id] = level
        
        if not competition["levels"]:
            print(f"⚠️  Warning: No levels found in competition {comp_id[:8]}, skipping")
            continue
        
        competitions[comp_id] = competition
        print(f"✓ Loaded competition {comp_id[:8]}...: {competition['name']} ({len(competition['levels'])} levels)")
    
    print(f"📊 Loaded {len(competitions)} competition(s)")
    return competitions


def _load_summary_md(competition_folder: Path) -> Optional[Dict[str, Any]]:
    """
    Loads and parses Summary.md from a competition folder.
    
    Args:
        competition_folder: Path to competition folder
        
    Returns:
        Dictionary with parsed sections, or None if file doesn't exist
    """
    summary_path = competition_folder / "Summary.md"
    
    if not summary_path.exists():
        print(f"⚠️  Warning: No Summary.md found in '{competition_folder.name}'")
        return None
    
    try:
        with open(summary_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse markdown sections
        summary = {}
        
        # Extract sections using regex to find markdown headers (## and ###)
        # Sections we're looking for:
        sections = {
            "overview": r"##\s+Overview\s*\n(.*?)(?=\n##|\Z)",
            "story": r"##\s+Story\s*\n(.*?)(?=\n##|\Z)",
            "level_progression": r"##\s+Level Progression\s*\n(.*?)(?=\n##|\Z)",
            "learning_objectives": r"##\s+Learning Objectives\s*\n(.*?)(?=\n##|\Z)",
            "difficulty_curve": r"##\s+Difficulty Curve\s*\n(.*?)(?=\n##|\Z)",
            "context": r"##\s+Context\s*\n(.*?)(?=\n##|\Z)",
            "estimated_time": r"##\s+Estimated Time\s*\n(.*?)(?=\n##|\Z)",
        }
        
        for section_key, pattern in sections.items():
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                section_content = match.group(1).strip()
                # Clean up extra whitespace
                section_content = re.sub(r'\n{3,}', '\n\n', section_content)
                summary[section_key] = section_content
            else:
                # Optional sections can be None
                if section_key in ["difficulty_curve", "context", "estimated_time"]:
                    summary[section_key] = None
                else:
                    # Required sections should warn if missing
                    print(f"⚠️  Warning: Missing required section '{section_key}' in Summary.md for '{competition_folder.name}'")
                    summary[section_key] = None
        
        return summary
        
    except Exception as e:
        print(f"⚠️  Warning: Error reading Summary.md in '{competition_folder.name}': {e}")
        return None

