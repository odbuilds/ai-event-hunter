# Hunt Events

Search for AI events and post a digest to Telegram. Follow these steps exactly.

## Step 1: Read state

Read `~/source/ai_event_hunter/state.json`. Note the `seen_event_ids` list.

## Step 2: Search for events

Use WebSearch for each of these queries:
- "AI events Belgrade Serbia 2026"
- "machine learning meetup Serbia 2026"
- "AI conference Serbia 2026 site:lu.ma OR site:meetup.com OR site:eventbrite.com"
- "LLM meetup Novi Sad Belgrade 2026"
- "online AI webinar 2026 site:lu.ma"
- "online LLM summit 2026 site:meetup.com"
- "AI conference online virtual 2026 site:eventbrite.com"
- "artificial intelligence summit online 2026"

## Step 3: Filter and extract

Read `~/source/ai_event_hunter/config.py` and follow FILTER_INSTRUCTIONS exactly.
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
If 0 qualifying events found after filtering, stop here and output "No new events found."

## Step 5: Post the digest

```bash
cd ~/source/ai_event_hunter
source venv/bin/activate
python post_digest.py --events '<PASTE_YOUR_JSON_ARRAY_HERE>'
```

## Step 6: Commit state.json

```bash
cd ~/source/ai_event_hunter
git add state.json
git commit -m "state: hunt $(date +%Y-%m-%d)"
git push
```
