"""
history_manager.py
------------------
Manages local JSON persistence for resume analysis records.

Handles creating the storage directory, adding records, listing history,
retrieving specific items, deleting entries, and graceful recovery from
corrupt files.
"""

import os
import json
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Base directory for the data folder
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"


def _ensure_history_storage() -> None:
    """Ensures data directory and history.json file exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def _read_raw_history() -> List[Dict[str, Any]]:
    """
    Safely reads history entries from the JSON file.
    Recovers gracefully if the JSON file is malformed or corrupt.
    """
    _ensure_history_storage()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as e:
        # Gracefully back up corrupted file and reset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        corrupt_backup = DATA_DIR / f"history_corrupt_{timestamp}.json"
        try:
            shutil.copy(HISTORY_FILE, corrupt_backup)
        except Exception:
            pass

        # Reset main history file to empty list
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

        return []


def _write_raw_history(entries: List[Dict[str, Any]]) -> bool:
    """Writes the full list of history records to disk atomically."""
    _ensure_history_storage()
    try:
        temp_file = DATA_DIR / f"history_tmp_{uuid.uuid4().hex[:6]}.json"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
        # Atomic replace
        os.replace(temp_file, HISTORY_FILE)
        return True
    except Exception as e:
        print(f"Error saving history to disk: {e}")
        return False


def save_analysis(
    candidate_name: str,
    filename: str,
    match_result: Dict[str, Any],
    suggestions: List[Dict[str, str]],
    word_count: int = 0,
    page_count: int = 1,
    report_filename: Optional[str] = None
) -> str:
    """
    Saves a completed analysis result into persistent history.

    Args:
        candidate_name: Name of the resume owner.
        filename: Original PDF file name.
        match_result: Output from skill_matcher.compare_skills.
        suggestions: List of recommendation dicts from suggestions.py.
        word_count: Total words in the resume.
        page_count: Total pages in the resume.
        report_filename: Optional saved report PDF path.

    Returns:
        The generated unique record ID.
    """
    entries = _read_raw_history()
    entry_id = str(uuid.uuid4())
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_record = {
        "id": entry_id,
        "timestamp": now_str,
        "name": candidate_name.strip() or "Candidate",
        "filename": filename,
        "score": match_result.get("match_score", 0),
        "total_job_skills": match_result.get("total_job_skills", 0),
        "total_resume_skills": match_result.get("total_resume_skills", 0),
        "matched": match_result.get("matched", []),
        "missing": match_result.get("missing", []),
        "extra": match_result.get("extra", []),
        "matched_count": len(match_result.get("matched", [])),
        "missing_count": len(match_result.get("missing", [])),
        "extra_count": len(match_result.get("extra", [])),
        "category_breakdown": match_result.get("category_breakdown", {}),
        "suggestions": suggestions,
        "word_count": word_count,
        "page_count": page_count,
        "has_job_skills": match_result.get("has_job_skills", True),
        "report_filename": report_filename
    }

    # Prepend to list so newest appears first
    entries.insert(0, new_record)
    _write_raw_history(entries)
    return entry_id


def list_history() -> List[Dict[str, Any]]:
    """Returns all past analysis records, ordered with most recent first."""
    return _read_raw_history()


def get_history_by_id(entry_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a specific history entry by its unique ID."""
    entries = _read_raw_history()
    for entry in entries:
        if entry.get("id") == entry_id:
            return entry
    return None


def delete_history_by_id(entry_id: str) -> bool:
    """Deletes a single history record by its ID."""
    entries = _read_raw_history()
    filtered = [e for e in entries if e.get("id") != entry_id]
    if len(filtered) == len(entries):
        return False  # Record was not found
    return _write_raw_history(filtered)


def clear_history() -> bool:
    """Clears all stored history records."""
    return _write_raw_history([])
