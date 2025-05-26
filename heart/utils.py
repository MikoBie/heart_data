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


def extract_value(dct: dict) -> str:
    """Extract the value of the answers.

    Parameters
    ----------
    dct : dict
        a dictionary with fields, body, selectionId, score.

    Returns
    -------
    str
        a selected answer, either an integer or description.
    """
    return dct["selectionId"] if dct["selectionId"] else ", ".join(dct["body"])


def extract_first_element(lst: list) -> str:
    """Returns the first element from a list. If the list is empty, returns an empty string.

    Parameters
    ----------
    lst
        a list of strings.

    Returns
    -------
        a string with the first element of the list. If the list is empty, returns an empty string.
    """
    return lst[0] if lst else ""
