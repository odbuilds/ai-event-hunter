# Local Slash Command + Telegram Channel Approval — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the two CCR cloud routines with a `/hunt-events` slash command and automatic Telegram-based calendar approval via Claude Code Channels.

**Architecture:** A `.claude/commands/hunt-events.md` slash command runs the full hunt flow locally (web search → filter → post to Telegram → commit state). A project-level `.claude/CLAUDE.md` tells Claude how to handle incoming Telegram "add X Y" replies received via the official Telegram channel plugin — reading `state.json`, adding approved events to Google Calendar via the MCP connector, and committing state. No new Python code is written.

**Tech Stack:** Claude Code slash commands, Claude Code Channels (Telegram plugin), Google Calendar MCP connector, existing Python scripts (`post_digest.py`, `state_manager.py`, `telegram_api.py`)

---

### Task 1: Create the `.claude/` directory and `/hunt-events` slash command

**Files:**
- Create: `.claude/commands/hunt-events.md`

- [ ] **Step 1: Create the `.claude/commands/` directory**

```bash
mkdir -p ~/source/ai_event_hunter/.claude/commands
```

- [ ] **Step 2: Create `.claude/commands/hunt-events.md`**

Write this exact content to `~/source/ai_event_hunter/.claude/commands/hunt-events.md`:

```markdown
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
```

- [ ] **Step 3: Verify the command file exists**

```bash
cat ~/source/ai_event_hunter/.claude/commands/hunt-events.md
```

Expected: file contents printed without error.

- [ ] **Step 4: Commit**

```bash
cd ~/source/ai_event_hunter
git add .claude/commands/hunt-events.md
git commit -m "feat: add /hunt-events slash command"
```

---

### Task 2: Create `.claude/CLAUDE.md` with Telegram approval instructions

**Files:**
- Create: `.claude/CLAUDE.md`

- [ ] **Step 1: Create `.claude/CLAUDE.md`**

Write this exact content to `~/source/ai_event_hunter/.claude/CLAUDE.md`:

```markdown
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
- **Start:** `datetime_iso` in Europe/Belgrade timezone
- **End:** `datetime_iso` + 1 hour, in Europe/Belgrade timezone
- **Location:** `location`
- **Description:** `url`

### Step 4: Update and commit state

Remove each approved event from `pending_events` in state.json. Save the file using the state_manager:

```bash
cd ~/source/ai_event_hunter
git add state.json
git commit -m "state: approve $(date +%Y-%m-%d)"
git push
```
```

- [ ] **Step 2: Verify the file exists**

```bash
cat ~/source/ai_event_hunter/.claude/CLAUDE.md
```

Expected: file contents printed without error.

- [ ] **Step 3: Commit**

```bash
cd ~/source/ai_event_hunter
git add .claude/CLAUDE.md
git commit -m "feat: add project CLAUDE.md with Telegram approval instructions"
```

---

### Task 3: Update AGENTS.md

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Replace the contents of `AGENTS.md`**

Write this exact content to `~/source/ai_event_hunter/AGENTS.md`:

```markdown
# AI Event Hunter — How to Run

## One-time setup

### 1. Install the Telegram channel plugin

In Claude Code, run:
```
/plugin install telegram@claude-plugins-official
```

### 2. Configure your bot token

```
/telegram:configure 8761241395:AAGixq48w6sumLD-lKt40ZWkTU77Ioa8fNM
```

### 3. Pair your Telegram account

Start Claude with the channel enabled:
```bash
claude --channels plugin:telegram@claude-plugins-official
```

Message your Telegram bot — it will reply with a pairing code. Then run:
```
/telegram:access pair <code>
/telegram:access policy allowlist
```

## Daily use

### Start Claude with Telegram channel

```bash
cd ~/source/ai_event_hunter
claude --channels plugin:telegram@claude-plugins-official
```

### Hunt for events

Run the slash command:
```
/hunt-events
```

Claude will search for events, post a digest to your Telegram channel, and commit state.json.

### Approve events

Reply to the digest in Telegram:
- `add 1 3` — approve events 1 and 3
- `add all` — approve all events

Claude will add approved events to the "AI Events" Google Calendar and commit state.json.
```

- [ ] **Step 2: Verify**

```bash
cat ~/source/ai_event_hunter/AGENTS.md
```

Expected: new content shown with setup and daily use instructions.

- [ ] **Step 3: Commit**

```bash
cd ~/source/ai_event_hunter
git add AGENTS.md
git commit -m "docs: update AGENTS.md for local slash command workflow"
```

---

### Task 4: Verify the slash command appears in Claude Code

- [ ] **Step 1: Restart Claude Code in the project directory**

```bash
cd ~/source/ai_event_hunter
claude
```

- [ ] **Step 2: Check the command is listed**

Type `/hunt` in the Claude Code prompt and verify that `/hunt-events` appears as an autocomplete option.

- [ ] **Step 3: Done**

The implementation is complete. To use the full workflow, start Claude with:

```bash
claude --channels plugin:telegram@claude-plugins-official
```

Then run `/hunt-events` to post a digest and reply "add X" in Telegram to approve events.
