import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("TELEGRAM_CHANNEL_ID", "-100123456")


def _reload():
    import importlib, telegram_api
    importlib.reload(telegram_api)
    return telegram_api


def test_post_message_returns_message_id():
    ta = _reload()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"result": {"message_id": 42}}
    with patch("telegram_api.requests.post", return_value=mock_resp) as mock_post:
        result = ta.post_message("hello world")
        assert result == 42
        call_kwargs = mock_post.call_args[1]["json"]
        assert call_kwargs["chat_id"] == "-100123456"
        assert call_kwargs["text"] == "hello world"


def test_get_updates_returns_update_list():
    ta = _reload()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"result": [{"update_id": 1, "message": {"text": "add 1"}}]}
    with patch("telegram_api.requests.get", return_value=mock_resp):
        result = ta.get_updates(offset=0)
        assert len(result) == 1
        assert result[0]["update_id"] == 1


def test_get_updates_passes_offset():
    ta = _reload()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"result": []}
    with patch("telegram_api.requests.get", return_value=mock_resp) as mock_get:
        ta.get_updates(offset=55)
        params = mock_get.call_args[1]["params"]
        assert params["offset"] == 55
