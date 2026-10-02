"""Load and save student records. All JSON file access lives here."""

from __future__ import annotations

import json
from pathlib import Path

from models import Student

DATA_FILE = Path(__file__).parent / "data" / "students.json"


def load_data(path: Path = DATA_FILE) -> tuple[list[Student], int, str | None]:
    """Load students and the next free id from the JSON file.

    Returns (students, next_id, warning). The file and its folder are
    created if missing. If the file is empty or corrupt, an empty list is
    returned with a warning message instead of crashing.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            save_data([], 1, path)
            return [], 1, None
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        students = [Student.from_dict(item) for item in raw["students"]]
        next_id = int(raw["next_id"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return [], 1, "Data file is empty or corrupt. Starting with no students."
    except OSError as error:
        return [], 1, f"Could not read data file: {error}"
    return students, max(next_id, max((s.id for s in students), default=0) + 1), None


def save_data(students: list[Student], next_id: int, path: Path = DATA_FILE) -> str | None:
    """Save students and next_id to the JSON file.

    Returns None on success, or an error message if saving failed.
    """
    payload = {"next_id": next_id, "students": [s.to_dict() for s in students]}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except OSError as error:
        return f"Could not save data file: {error}"
    return None