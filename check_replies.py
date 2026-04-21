"""
CLI: python check_replies.py
Called by approve agent. Checks Telegram for "add X Y" replies, adds approved events to Google Calendar.
"""
import re
from datetime import datetime, timedelta

from calendar_api import add_event, create_calendar
from state_manager import load_state, save_state
from telegram_api import get_updates


def parse_add_command(text):
    """Return list of int event numbers, 'all', or [] if not an add command."""
    text = (text or "").strip().lower()
    if not text.startswith("add"):
        return []
    rest = text[3:].strip()
    if rest == "all":
        return "all"
    nums = re.findall(r"\d+", rest)
    return [int(n) for n in nums] if nums else []


def _end_iso(start_iso):
    return (datetime.fromisoformat(start_iso) + timedelta(hours=1)).isoformat()


def main():
    state = load_state()
    updates = get_updates(offset=state.get("telegram_offset", 0))

    if not updates:
        print("No new Telegram updates.")
        return

    state["telegram_offset"] = updates[-1]["update_id"] + 1

    if not state.get("ai_calendar_id"):
        state["ai_calendar_id"] = create_calendar("AI Events")
        print(f"Created 'AI Events' calendar: {state['ai_calendar_id']}")

    pending = state.get("pending_events", {})
    changed = False

    for update in updates:
        msg = update.get("message") or update.get("channel_post")
        if not msg:
            continue
        approved = parse_add_command(msg.get("text", ""))
        if not approved:
            continue

        keys = list(pending.keys()) if approved == "all" else [str(n) for n in approved]
        for key in keys:
            if key not in pending:
                print(f"No pending event #{key}, skipping")
                continue
            ev = pending[key]
            start_iso = ev.get("datetime_iso") or datetime.now().replace(
                hour=18, minute=0, second=0, microsecond=0
            ).isoformat()
            try:
                add_event(
                    state["ai_calendar_id"],
                    ev["name"],
                    start_iso,
                    _end_iso(start_iso),
                    ev.get("location", "Online"),
                    ev["url"],
                )
                print(f"✅ Added to calendar: {ev['name']}")
                del pending[key]
                changed = True
            except Exception as exc:
                print(f"❌ Failed to add {ev['name']}: {exc}")

    state["pending_events"] = pending
    if changed or updates:
        save_state(state)


if __name__ == "__main__":
    main()
