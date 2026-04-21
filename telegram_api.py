import os
import requests
from dotenv import load_dotenv

load_dotenv()


def _base():
    return f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}"


def _channel():
    return os.environ["TELEGRAM_CHANNEL_ID"]


def post_message(text):
    resp = requests.post(f"{_base()}/sendMessage", json={"chat_id": _channel(), "text": text})
    resp.raise_for_status()
    return resp.json()["result"]["message_id"]


def get_updates(offset=0):
    resp = requests.get(f"{_base()}/getUpdates", params={"offset": offset, "timeout": 5})
    resp.raise_for_status()
    return resp.json()["result"]
