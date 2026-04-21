"""
CLI: python post_digest.py --events '<json_array>' [--date '21 Apr']
Called by hunt agent after discovering events.
"""
import argparse
import json
from datetime import date

from config import MAX_EVENTS_PER_DIGEST
from state_manager import load_state, save_state
from telegram_api import post_message


def format_digest(events, date_str):
    lines = [f"🤖 AI Events — {date_str}\n"]
    for i, ev in enumerate(events, 1):
        tag = f"In-person, {ev['location']}" if ev["type"] == "in-person" else "Online"
        lines.append(f"{i}. {ev['name']} — {tag} | {ev['date']} | {ev['url']}")
    lines.append('\nReply "add 1 3" to approve, or ignore to skip')
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", required=True, help="JSON array of event objects")
    parser.add_argument("--date", default=date.today().strftime("%-d %b"))
    args = parser.parse_args()

    events = json.loads(args.events)
    state = load_state()

    new_events = [e for e in events if e["url"] not in state["seen_event_ids"]]
    new_events = sorted(new_events, key=lambda e: e.get("datetime_iso", ""))[:MAX_EVENTS_PER_DIGEST]

    if not new_events:
        print("No new events to post.")
        return

    digest = format_digest(new_events, args.date)
    message_id = post_message(digest)
    print(f"Posted digest (message_id={message_id}) with {len(new_events)} events")

    state["pending_events"] = {}
    for i, ev in enumerate(new_events, 1):
        state["pending_events"][str(i)] = {**ev, "message_id": message_id}
        if ev["url"] not in state["seen_event_ids"]:
            state["seen_event_ids"].append(ev["url"])

    save_state(state)


if __name__ == "__main__":
    main()
