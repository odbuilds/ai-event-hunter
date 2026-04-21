import json
import pytest
from pathlib import Path
from unittest.mock import patch


def test_load_state_returns_defaults_when_no_file(tmp_path):
    state_file = tmp_path / "state.json"
    with patch("state_manager.STATE_FILE", state_file):
        import importlib, state_manager
        importlib.reload(state_manager)
        result = state_manager.load_state()
        assert result["seen_event_ids"] == []
        assert result["pending_events"] == {}
        assert result["telegram_offset"] == 0
        assert result["ai_calendar_id"] is None


def test_save_and_load_roundtrip(tmp_path):
    state_file = tmp_path / "state.json"
    with patch("state_manager.STATE_FILE", state_file):
        import importlib, state_manager
        importlib.reload(state_manager)
        data = {
            "seen_event_ids": ["https://lu.ma/test"],
            "pending_events": {"1": {"name": "AI Summit", "url": "https://lu.ma/test"}},
            "telegram_offset": 99,
            "ai_calendar_id": "cal@group.calendar.google.com",
        }
        state_manager.save_state(data)
        result = state_manager.load_state()
        assert result == data
