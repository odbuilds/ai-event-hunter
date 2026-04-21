from post_digest import format_digest


def test_format_digest_header():
    events = [{"name": "AI Summit", "type": "in-person", "location": "Belgrade",
               "date": "May 15, 18:00", "datetime_iso": "2026-05-15T18:00:00", "url": "https://lu.ma/x"}]
    result = format_digest(events, "15 May")
    assert "🤖 AI Events — 15 May" in result


def test_format_digest_in_person_line():
    events = [{"name": "AI Summit", "type": "in-person", "location": "Belgrade",
               "date": "May 15, 18:00", "datetime_iso": "2026-05-15T18:00:00", "url": "https://lu.ma/x"}]
    result = format_digest(events, "15 May")
    assert "1. AI Summit — In-person, Belgrade | May 15, 18:00 | https://lu.ma/x" in result


def test_format_digest_online_line():
    events = [{"name": "LLM Webinar", "type": "online", "location": "Online",
               "date": "May 17, 20:00", "datetime_iso": "2026-05-17T20:00:00", "url": "https://meetup.com/y"}]
    result = format_digest(events, "17 May")
    assert "1. LLM Webinar — Online | May 17, 20:00 | https://meetup.com/y" in result


def test_format_digest_reply_footer():
    events = [{"name": "X", "type": "online", "location": "Online",
               "date": "May 1", "datetime_iso": "2026-05-01T18:00:00", "url": "https://x.com"}]
    result = format_digest(events, "1 May")
    assert 'Reply "add 1 3" to approve' in result


def test_format_digest_multiple_events_numbered():
    events = [
        {"name": "Event A", "type": "online", "location": "Online", "date": "May 1", "datetime_iso": "2026-05-01T18:00:00", "url": "https://a.com"},
        {"name": "Event B", "type": "in-person", "location": "Novi Sad", "date": "May 2", "datetime_iso": "2026-05-02T18:00:00", "url": "https://b.com"},
    ]
    result = format_digest(events, "1 May")
    assert "1. Event A" in result
    assert "2. Event B" in result
