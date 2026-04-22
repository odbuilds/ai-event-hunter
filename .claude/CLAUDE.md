# AI Event Hunter — Project Instructions

## Handling Telegram approval replies

When you receive a message via the Telegram channel that starts with "add" (e.g. "add 1 3" or "add all"), follow these steps exactly:

### Step 1: Parse the command

- "add all" → approve every event in pending_events
- "add 1 3" → approve events numbered 1 and 3
- Any other message → ignore it silently

### Step 2: Read state

Read `~/source/ai_event_hunter/state.json`. Look up each approved number in `pending_events`.

### Step 3: Add to Google Calendar

For each approved event, add it to the "AI Events" Google Calendar using the Google Calendar MCP connector. Create the calendar if it does not exist.

Use these fields:
- **Title:** `name`
- **Start:** `datetime_iso` value with timezone `Europe/Belgrade`
- **End:** `datetime_iso` + 1 hour, timezone `Europe/Belgrade`
- **Location:** `location`
- **Description:** `url`
- **Timezone:** `Europe/Belgrade` (pass this explicitly to the connector)

### Step 4: Update and commit state

Remove each approved event from `pending_events` in state.json. Save the file, then:

```bash
cd ~/source/ai_event_hunter
git add state.json
git commit -m "state: approve $(date +%Y-%m-%d)"
git push
```
