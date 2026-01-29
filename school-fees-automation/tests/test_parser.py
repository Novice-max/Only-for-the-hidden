import pytest

from app.mpesa.parser import parse_reference


def test_parse_reference_pipe_separator():
    assert parse_reference("041|1043") == ["041", "1043"]


def test_parse_reference_comma_separator():
    assert parse_reference("041,1043") == ["041", "1043"]


def test_parse_reference_invalid_character():
    with pytest.raises(ValueError):
        parse_reference("041 & 1043")


def test_parse_reference_duplicate_parts():
    with pytest.raises(ValueError):
        parse_reference("041|041")


def test_parse_reference_empty_input():
    with pytest.raises(ValueError):
        parse_reference("")


def test_parse_reference_non_numeric():
    with pytest.raises(ValueError):
        parse_reference("041|10A")
