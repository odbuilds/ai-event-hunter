# AI Event Hunter

Discovers AI events (in-person in Serbia, online globally) and sends a digest to Telegram every Mon/Wed/Fri. Reply "add 1 3" to add events to your "AI Events" Google Calendar. No laptop needs to be on — runs via Claude Code cloud scheduled agents.

## How it works

1. **Hunt agent** (Mon/Wed/Fri 9am CET): searches Luma, Meetup, Eventbrite, and the web for AI events → posts a numbered digest to your Telegram channel
2. You reply "add 1" or "add 1 3" or "add all" to approve events
3. **Approve agent** (once daily): sees your reply → adds events to your "AI Events" Google Calendar via connector

## Setup

### Prerequisites
- Python 3.11+
- A GitHub repo for this project (for state persistence between cloud agent runs)
- Claude Code with Google Calendar connector enabled (claude.ai → Connectors)
- Claude Code cloud scheduled tasks enabled

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

### 3. Schedule agents

Use the Claude Code **Schedule** page (Desktop app or cloud) to create two cloud tasks:

**Hunt agent** (searches and posts events):
- Prompt: `Read and follow exactly the instructions in HUNT_AGENT.md`
- Schedule: Mon/Wed/Fri at 9am CET
- Env vars: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_ID`
- Connector: none needed

**Approve agent** (processes replies, adds to calendar):
- Prompt: `Read and follow exactly the instructions in APPROVE_AGENT.md`
- Schedule: Daily at 6pm CET
- Env vars: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_ID`
- Connector: Google Calendar (already connected at claude.ai)

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

The next daily approve run will add approved events to your "AI Events" Google Calendar.

## Customising search

Edit `config.py`:
- `SEARCH_QUERIES` — add or change what gets searched
- `FILTER_INSTRUCTIONS` — tune what the agent includes/excludes

## Tests

```bash
source venv/bin/activate
pytest tests/ -v
```
