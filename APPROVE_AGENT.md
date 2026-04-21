# Approve Agent — Instructions

Runs once daily. Follow these steps exactly.

## Step 1: Check for replies
```bash
cd ~/source/ai_event_hunter
source venv/bin/activate
python check_replies.py
```

If output is "No new Telegram updates." or "No approvals found." — stop here. No commit needed.

## Step 2: Add approved events to Google Calendar
If the script printed a JSON array of events, add each one to the "AI Events" Google Calendar using the Google Calendar connector.

For each event in the JSON output:
- **Title:** `name`
- **Start:** `start_iso` (Europe/Belgrade timezone)
- **End:** `end_iso` (Europe/Belgrade timezone)
- **Location:** `location`
- **Description:** `url`

## Step 3: Commit state.json
```bash
cd ~/source/ai_event_hunter
git add state.json
git commit -m "state: approve $(date +%Y-%m-%d)"
git push
```
