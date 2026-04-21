import os
import requests
from dotenv import load_dotenv

load_dotenv()

_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
_CHANNEL = os.environ["TELEGRAM_CHANNEL_ID"]
_BASE = f"https://api.telegram.org/bot{_TOKEN}"


def post_message(text):
    resp = requests.post(f"{_BASE}/sendMessage", json={"chat_id": _CHANNEL, "text": text})
    resp.raise_for_status()
    return resp.json()["result"]["message_id"]


def get_updates(offset=0):
    resp = requests.get(f"{_BASE}/getUpdates", params={"offset": offset, "timeout": 5})
    resp.raise_for_status()
    return resp.json()["result"]
