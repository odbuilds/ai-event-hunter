"""
Run once to verify your bot token and channel access.
Usage: python setup_telegram.py
Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID in .env
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.environ["TELEGRAM_BOT_TOKEN"]
channel = os.environ.get("TELEGRAM_CHANNEL_ID", "")
base = f"https://api.telegram.org/bot{token}"

me = requests.get(f"{base}/getMe").json()
if not me.get("ok"):
    print(f"❌ Bad token: {me}")
    raise SystemExit(1)
print(f"✅ Bot verified: @{me['result']['username']}")

if not channel:
    print("\nTELEGRAM_CHANNEL_ID not set yet.")
    print("After creating your channel and adding the bot as admin, send any message in it, then run:")
    print(f"  curl https://api.telegram.org/bot{token}/getUpdates")
    print("Look for 'chat' > 'id' in the result — that's your channel ID (will be negative).")
else:
    r = requests.post(f"{base}/sendMessage", json={"chat_id": channel, "text": "✅ AI Event Hunter connected!"})
    if r.ok:
        print(f"✅ Test message posted to channel {channel}")
    else:
        print(f"❌ Failed to post: {r.json()}")
