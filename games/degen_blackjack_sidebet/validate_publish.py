"""Validate generated publish files against documented Stake Engine math requirements."""

from __future__ import annotations

import csv
import json
from pathlib import Path

REQUIRED_MODE_KEYS = {"name", "cost", "events", "weights"}
REQUIRED_BOOK_KEYS = {"id", "events", "payoutMultiplier"}


class ValidationError(Exception):
    """Raised when the generated publish files do not match expectations."""



def validate_lookup_csv(csv_path: Path) -> None:
    """Validate the published lookup table structure."""
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for row_number, row in enumerate(reader, start=1):
            if len(row) != 3:
                raise ValidationError(f"{csv_path} row {row_number} must contain exactly 3 columns")
            for value in row:
                int(value)



def validate_jsonl_books(book_path: Path) -> None:
    """Validate an uncompressed jsonl book file when present."""
    with book_path.open("r", encoding="utf-8") as handle:
        first_line = handle.readline().strip()
    if not first_line:
        raise ValidationError(f"{book_path} is empty")
    payload = json.loads(first_line)
    missing = REQUIRED_BOOK_KEYS - payload.keys()
    if missing:
        raise ValidationError(f"{book_path} is missing required keys: {sorted(missing)}")



def validate_index(index_path: Path) -> list[dict]:
    """Validate the published index.json structure and return modes."""
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    modes = payload.get("modes")
    if not isinstance(modes, list) or not modes:
        raise ValidationError("index.json must contain a non-empty 'modes' list")

    for mode in modes:
        if not isinstance(mode, dict):
            raise ValidationError("each mode entry in index.json must be an object")
        missing = REQUIRED_MODE_KEYS - mode.keys()
        if missing:
            raise ValidationError(f"mode entry is missing required keys: {sorted(missing)}")
    return modes



def validate_publish_folder(publish_dir: Path) -> None:
    """Validate a Stake Engine publish directory."""
    index_path = publish_dir / "index.json"
    if not index_path.exists():
        raise ValidationError(f"missing required file: {index_path}")

    modes = validate_index(index_path)
    for mode in modes:
        weights_path = publish_dir / mode["weights"]
        events_path = publish_dir / mode["events"]

        if not weights_path.exists():
            raise ValidationError(f"missing lookup CSV for mode '{mode['name']}': {weights_path}")
        if not events_path.exists():
            raise ValidationError(f"missing event file for mode '{mode['name']}': {events_path}")
        if events_path.suffixes[-2:] != [".jsonl", ".zst"]:
            raise ValidationError(f"event file for mode '{mode['name']}' must end with .jsonl.zst")

        validate_lookup_csv(weights_path)

        uncompressed_candidate = publish_dir.parent / "books" / events_path.name.replace(".jsonl.zst", ".jsonl")
        if uncompressed_candidate.exists():
            validate_jsonl_books(uncompressed_candidate)



def main() -> None:
    publish_dir = Path(__file__).resolve().parent / "library" / "publish_files"
    validate_publish_folder(publish_dir)
    print(f"Publish files look valid: {publish_dir}")


if __name__ == "__main__":
    main()
