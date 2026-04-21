import os
import requests
from dotenv import load_dotenv

load_dotenv()

_TOKEN_URL = "https://oauth2.googleapis.com/token"
_CAL_BASE = "https://www.googleapis.com/calendar/v3"


def _get_access_token():
    resp = requests.post(_TOKEN_URL, data={
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]


def _auth_headers():
    return {"Authorization": f"Bearer {_get_access_token()}"}


def create_calendar(name="AI Events"):
    resp = requests.post(
        f"{_CAL_BASE}/calendars",
        headers=_auth_headers(),
        json={"summary": name},
    )
    resp.raise_for_status()
    return resp.json()["id"]


def add_event(calendar_id, title, start_iso, end_iso, location, url):
    resp = requests.post(
        f"{_CAL_BASE}/calendars/{calendar_id}/events",
        headers=_auth_headers(),
        json={
            "summary": title,
            "location": location,
            "description": url,
            "start": {"dateTime": start_iso, "timeZone": "Europe/Belgrade"},
            "end": {"dateTime": end_iso, "timeZone": "Europe/Belgrade"},
        },
    )
    resp.raise_for_status()
    return resp.json()["id"]
