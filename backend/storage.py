import json
import uuid
from pathlib import Path
from datetime import datetime, timezone
from .schemas import PLATFORMS, DAILY_TARGETS

LOG_PATH = Path(__file__).parent / "outreach_log.json"


def _load() -> list:
    if LOG_PATH.exists():
        try:
            return json.loads(LOG_PATH.read_text())
        except Exception:
            return []
    return []


def _save(entries: list) -> None:
    LOG_PATH.write_text(json.dumps(entries, indent=2))


def add_entry(entry: dict) -> dict:
    entries = _load()
    entry = {**entry, "id": str(uuid.uuid4())[:8]}
    entries.append(entry)
    _save(entries)
    return entry


def all_entries() -> list:
    return _load()


def delete_entry(entry_id: str) -> bool:
    entries = _load()
    remaining = [e for e in entries if e["id"] != entry_id]
    if len(remaining) == len(entries):
        return False
    _save(remaining)
    return True


def daily_progress() -> dict:
    """Counts of messages logged today, per platform, against daily targets."""
    today = datetime.now(timezone.utc).date().isoformat()
    entries = [e for e in _load() if e.get("date") == today]

    counts = {p: 0 for p in PLATFORMS}
    for e in entries:
        if e.get("platform") in counts:
            counts[e["platform"]] += 1

    return {
        p: {"sent": counts[p], "target": DAILY_TARGETS[p]}
        for p in PLATFORMS
    }
