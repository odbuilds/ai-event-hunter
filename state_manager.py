import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "state.json"

DEFAULT_STATE = {
    "seen_event_ids": [],
    "pending_events": {},
    "telegram_offset": 0,
    "ai_calendar_id": None,
}


def load_state():
    if not STATE_FILE.exists():
        return DEFAULT_STATE.copy()
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
