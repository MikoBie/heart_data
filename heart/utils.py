import datetime


def date_quarter(created: str) -> str:
    """Simplify the created date to a YYYY-QQ format.

    Parameters
    ----------
    created
        a string with the date in YYYY-MM-DDTHH:MM:SSZ format.

    Returns
    -------
        a string withe the date in YYYY-QQ format.
    """
    try:
        date = datetime.datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        date = datetime.datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%fZ")

    return f"{date.year}-{(date.month - 1) // 3 + 1:02d}"
