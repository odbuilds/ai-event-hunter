# Approve Agent — Instructions

Runs 3x daily: 9am, 1pm, 6pm CET. Follow these steps exactly.

## Step 1: Check for replies and process approvals
```bash
cd ~/source/ai_event_hunter
source venv/bin/activate
python check_replies.py
```
Read the output. Lines starting with ✅ mean events were added to Google Calendar.

## Step 2: Commit if state changed
Only commit if `check_replies.py` output showed updates (new updates found or events added):
```bash
cd ~/source/ai_event_hunter
git add state.json
git commit -m "state: approve $(date +%Y-%m-%d-%H%M)"
git push
```
If the output was "No new Telegram updates." — skip the commit.
