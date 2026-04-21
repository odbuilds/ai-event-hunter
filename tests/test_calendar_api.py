import pytest
from unittest.mock import patch, MagicMock, call


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "client_id")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "client_secret")
    monkeypatch.setenv("GOOGLE_REFRESH_TOKEN", "refresh_token")


def _reload():
    import importlib, calendar_api
    importlib.reload(calendar_api)
    return calendar_api


def _token_resp():
    m = MagicMock()
    m.json.return_value = {"access_token": "tok123"}
    return m


def test_create_calendar_returns_id():
    ca = _reload()
    cal_resp = MagicMock()
    cal_resp.json.return_value = {"id": "cal@group.calendar.google.com"}
    with patch("calendar_api.requests.post", side_effect=[_token_resp(), cal_resp]):
        result = ca.create_calendar("AI Events")
        assert result == "cal@group.calendar.google.com"


def test_add_event_returns_event_id():
    ca = _reload()
    event_resp = MagicMock()
    event_resp.json.return_value = {"id": "evt_abc"}
    with patch("calendar_api.requests.post", side_effect=[_token_resp(), event_resp]):
        result = ca.add_event(
            "cal@group.calendar.google.com",
            "AI Summit",
            "2026-05-15T18:00:00",
            "2026-05-15T19:00:00",
            "Belgrade",
            "https://lu.ma/ai",
        )
        assert result == "evt_abc"


def test_add_event_sends_correct_body():
    ca = _reload()
    event_resp = MagicMock()
    event_resp.json.return_value = {"id": "evt_abc"}
    with patch("calendar_api.requests.post", side_effect=[_token_resp(), event_resp]) as mock_post:
        ca.add_event("cal123", "AI Summit", "2026-05-15T18:00:00", "2026-05-15T19:00:00", "Belgrade", "https://lu.ma/ai")
        body = mock_post.call_args_list[1][1]["json"]
        assert body["summary"] == "AI Summit"
        assert body["location"] == "Belgrade"
        assert body["description"] == "https://lu.ma/ai"
        assert body["start"]["dateTime"] == "2026-05-15T18:00:00"
