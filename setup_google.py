"""
Run once locally to authorise Google Calendar access.
Requires google/.google-credentials.json from Google Cloud Console.

Steps to get google-credentials.json:
  1. Go to console.cloud.google.com → New project
  2. Enable 'Google Calendar API'
  3. Credentials → Create credentials → OAuth client ID → Desktop app
  4. Download JSON → save as google/.google-credentials.json

Usage: python setup_google.py
"""
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDS_FILE = Path(__file__).parent / "google" / ".google-credentials.json"

if not CREDS_FILE.exists():
    print(f"❌ Missing credentials file: {CREDS_FILE}")
    print("Follow the steps in this file's docstring to create it.")
    raise SystemExit(1)

flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_FILE), SCOPES)
creds = flow.run_local_server(port=0)

print("\n✅ Authorised. Add these three values to your .env and to the scheduled agent env vars:\n")
print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")
print(f"GOOGLE_CLIENT_ID={creds.client_id}")
print(f"GOOGLE_CLIENT_SECRET={creds.client_secret}")
