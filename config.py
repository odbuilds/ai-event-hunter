SEARCH_QUERIES = [
    "AI events Belgrade Serbia 2026",
    "machine learning meetup Serbia 2026",
    "AI conference Serbia 2026 site:lu.ma OR site:meetup.com OR site:eventbrite.com",
    "LLM meetup Novi Sad Belgrade 2026",
    "online AI webinar 2026 site:lu.ma",
    "online LLM summit 2026 site:meetup.com",
    "AI conference online virtual 2026 site:eventbrite.com",
    "artificial intelligence summit online 2026",
]

FILTER_INSTRUCTIONS = """
Include ONLY:
- In-person events physically located in Serbia (Belgrade, Novi Sad, or other Serbian cities)
- Online/virtual events on any AI, ML, LLM, or GenAI topic globally

Exclude:
- Marketing or sales webinars
- Events with no clear date
- Events on non-AI tech topics (DevOps, cybersecurity, etc.) unless AI is the main focus
- Company-specific product workshops (not educational)

For each event extract:
- name: full event title
- type: "in-person" or "online"
- location: city name for in-person (e.g. "Belgrade"), or "Online"
- date: human-readable date and time, e.g. "May 15, 18:00"
- datetime_iso: ISO 8601, e.g. "2026-05-15T18:00:00" — use 18:00 if no time given
- url: direct event URL
"""

MAX_EVENTS_PER_DIGEST = 10
