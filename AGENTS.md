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
