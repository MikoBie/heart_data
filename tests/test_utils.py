import pytest
from heart.utils import date_quarter, extract_value, extract_first_element


@pytest.mark.parametrize(
    "tpl",
    [
        ("2025-01-09T06:53:53.345Z", "2025-01"),
        ("2024-05-09T06:53:53Z", "2024-02"),
        ("2024-09-09T06:53:53.883Z", "2024-03"),
        ("2024-11-09T06:53:53Z", "2024-04"),
    ],
)
def test_date_quarter(tpl: tuple) -> None:
    date, output = tpl
    result = date_quarter(date)
    assert isinstance(result, str)
    assert result == output


@pytest.mark.parametrize(
    "dct",
    [
        {"selectionId": "123", "body": []},
        {"selectionId": "", "body": ["answer1", "answer2"]},
        {"selectionId": "456", "body": ["answer3"]},
    ],
)
def test_extract_value(dct: dict) -> None:
    result = extract_value(dct)
    assert isinstance(result, str)
    if dct["selectionId"]:
        assert result == dct["selectionId"]
    else:
        assert result == ", ".join(dct["body"])


@pytest.mark.parametrize(
    "lst",
    [
        ["first", "second"],
        ["only_one"],
        [],
    ],
)
def test_extract_first_element(lst: list) -> None:
    result = extract_first_element(lst)
    assert isinstance(result, str)
    if lst:
        assert result == lst[0]
    else:
        assert result == ""
