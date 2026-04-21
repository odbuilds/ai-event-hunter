# AI Event Hunter

Discovers AI events (in-person in Serbia, online globally) and sends a digest to Telegram every Mon/Wed/Fri. Reply "add 1 3" to add events to your "AI Events" Google Calendar. No laptop needs to be on — runs via Claude Code scheduled agents.

## How it works

1. **Hunt agent** (Mon/Wed/Fri 9am CET): searches Luma, Meetup, Eventbrite, and the web for AI events → posts a numbered digest to your Telegram channel
2. You reply "add 1" or "add 1 3" or "add all" to approve events
3. **Approve agent** (3x daily: 9am, 1pm, 6pm CET): sees your reply → adds events to Google Calendar

## Setup

### Prerequisites
- Python 3.11+
- A GitHub repo for this project (for state persistence between cloud agent runs)
- Claude Code with scheduled agents enabled

### Install

```bash
cd ~/source/ai_event_hunter
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 1. Create a GitHub repo

Create a private repo at github.com, then:

```bash
cd ~/source/ai_event_hunter
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-event-hunter.git
git push -u origin main
```

### 2. Telegram bot

1. Open Telegram → search `@BotFather` → `/newbot` → follow prompts → copy the bot token
2. Set `TELEGRAM_BOT_TOKEN=<token>` in `.env`
3. Create a new private channel in Telegram
4. Add your bot as admin (Channel Settings → Administrators → Add Administrator)
5. Send any message in the channel, then run:
   ```bash
   source venv/bin/activate
   python setup_telegram.py
   ```
6. Follow the printed instructions to get your channel ID, add it to `.env` as `TELEGRAM_CHANNEL_ID`
7. Run `python setup_telegram.py` again — should print "Test message posted ✅"

### 3. Google Calendar

1. Go to [console.cloud.google.com](https://console.cloud.google.com) → New project
2. Enable **Google Calendar API**
3. Credentials → Create credentials → OAuth client ID → Desktop app → Download JSON
4. Save the downloaded file as `google/.google-credentials.json`
5. Run:
   ```bash
   source venv/bin/activate
   python setup_google.py
   ```
6. Complete the browser auth flow
7. Copy the three printed values into `.env`:
   - `GOOGLE_REFRESH_TOKEN`
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`

### 4. Schedule agents

Use the Claude Code `schedule` skill to create two triggers:

**Hunt agent** (searches and posts events):
- Prompt: `Read and follow exactly the instructions in ~/source/ai_event_hunter/HUNT_AGENT.md`
- Schedule: `0 8 * * 1,3,5` (Mon/Wed/Fri 8am UTC = 9am CET)
- Env vars: all five from `.env`

**Approve agent** (processes replies, adds to calendar):
- Prompt: `Read and follow exactly the instructions in ~/source/ai_event_hunter/APPROVE_AGENT.md`
- Schedule: `0 8,12,17 * * *` (8am, 12pm, 5pm UTC)
- Env vars: all five from `.env`

## Usage

When a digest arrives in your Telegram channel:

```
🤖 AI Events — 21 Apr

1. AI Summit — In-person, Belgrade | May 15, 18:00 | lu.ma/...
2. LLM Webinar — Online | May 17, 20:00 | meetup.com/...

Reply "add 1 3" to approve, or ignore to skip
```

Reply with:
- `add 1` — add event 1
- `add 1 3` — add events 1 and 3
- `add all` — add everything

The next approve agent run (within a few hours) will add approved events to your "AI Events" Google Calendar.

## Customising search

Edit `config.py`:
- `SEARCH_QUERIES` — add or change what gets searched
- `FILTER_INSTRUCTIONS` — tune what the agent includes/excludes

## Tests

```bash
source venv/bin/activate
pytest tests/ -v
```
