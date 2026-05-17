# Hunt Agent — Instructions

Runs Mon/Wed/Fri at 9am CET. All paths are relative to the repo root (the current working directory). Follow these steps exactly. Do not skip steps. Do not edit `state.json` directly — only `post_digest.py` may write `pending_events`.

## Step 1: Read state
Read `state.json` from the current directory. Note the `seen_event_ids` list.

## Step 2: Search for events
Use WebSearch for each of these queries:
- "AI events Belgrade Serbia 2026"
- "machine learning meetup Serbia 2026"
- "AI conference Serbia 2026 site:lu.ma OR site:meetup.com"
- "LLM meetup Novi Sad Belgrade 2026"
- "online AI webinar 2026 site:lu.ma"
- "online LLM summit 2026 site:meetup.com"
- "AI conference online virtual 2026 site:eventbrite.com"
- "artificial intelligence summit online 2026"

## Step 3: Filter and extract
Read `config.py` and follow FILTER_INSTRUCTIONS exactly.
Exclude any event whose URL is already in `seen_event_ids`.

## Step 4: Build the JSON array
Create a JSON array of up to 10 events sorted by `datetime_iso` ascending:
```json
[
  {
    "name": "Event Title",
    "type": "in-person",
    "location": "Belgrade",
    "date": "May 15, 18:00",
    "datetime_iso": "2026-05-15T18:00:00",
    "url": "https://lu.ma/event-slug"
  }
]
```
If 0 qualifying events are found after filtering, stop here and output "No new events found." Do not touch `state.json`.

## Step 5: Post the digest (mandatory)
Write the JSON array to `/tmp/events.json` first, then invoke the script from the repo root. Do not `cd` anywhere, do not activate a venv — `python3` from the repo root is correct.

```bash
python3 post_digest.py --events "$(cat /tmp/events.json)"
```

The script will (a) POST to Telegram, (b) capture the returned `message_id`, (c) write `pending_events` to `state.json`. If the Telegram call fails, the script raises and `state.json` is NOT modified — that is the correct behaviour.

## Step 6: Verify the post succeeded
Run this verification — it MUST pass before continuing:

```bash
python3 -c "
import json, sys, os, urllib.request, urllib.parse
state = json.load(open('state.json'))
pending = state.get('pending_events', {})
if not pending:
    print('VERIFY: no pending events — nothing to verify'); sys.exit(0)
bad = [k for k, v in pending.items() if not v.get('message_id')]
if bad:
    token = os.environ['TELEGRAM_BOT_TOKEN']
    chat = os.environ['TELEGRAM_CHANNEL_ID']
    urllib.request.urlopen(f'https://api.telegram.org/bot{token}/sendMessage',
        data=urllib.parse.urlencode({'chat_id': chat,
            'text': f'Hunt FAILED: pending_events entries {bad} have no Telegram message_id. post_digest.py was not invoked correctly.'}).encode())
    sys.exit(f'VERIFY FAILED: entries {bad} missing message_id')
print(f'VERIFY OK: {len(pending)} pending event(s), all have message_id')
"
```

If verification fails, stop and report — do not commit.

## Step 7: Commit state.json
```bash
git add state.json
git commit -m "state: hunt $(date +%Y-%m-%d)"
git push
```
