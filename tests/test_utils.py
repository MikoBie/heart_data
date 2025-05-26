import pytest
from heart.utils import date_quarter


@pytest.mark.parametrize(
    "pair",
    [
        ("2025-01-09T06:53:53.345Z", "2025-01"),
        ("2024-05-09T06:53:53Z", "2024-02"),
        ("2024-09-09T06:53:53.883Z", "2024-03"),
        ("2024-11-09T06:53:53Z", "2024-04"),
    ],
)
def test_date_quarter(pair: tuple) -> None:
    date, output = pair
    result = date_quarter(date)
    assert isinstance(result, str)
    assert result == output
