from check_replies import parse_add_command, _end_iso


def test_parse_add_single_number():
    assert parse_add_command("add 1") == [1]


def test_parse_add_multiple_numbers():
    assert parse_add_command("add 1 3") == [1, 3]


def test_parse_add_all():
    assert parse_add_command("add all") == "all"


def test_parse_non_add_returns_empty():
    assert parse_add_command("yes please") == []
    assert parse_add_command("") == []
    assert parse_add_command("ignore") == []
    assert parse_add_command(None) == []


def test_parse_case_insensitive():
    assert parse_add_command("ADD 2") == [2]
    assert parse_add_command("Add All") == "all"


def test_parse_add_with_extra_whitespace():
    assert parse_add_command("  add  1  3  ") == [1, 3]


def test_end_iso_adds_one_hour():
    result = _end_iso("2026-05-15T18:00:00")
    assert result == "2026-05-15T19:00:00"
