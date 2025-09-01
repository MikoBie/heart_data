import datetime
from collections.abc import Callable


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


def round_label(x: float) -> str:
    """Rounds a float to the nearest integer and converts it to a string with %. If the result is 0, it return "".

    Parameters
    ----------
    x
        a float number.

    Returns
    -------
        a string with the rounded integer.
    """
    return f"{(int(round(x, 0)))}%" if int(round(x, 0)) != 0 else ""


def process_lst(lst: list, func: Callable[[], float] = lambda x: min) -> list[float]:
    """Applies the func to each element of the list. It returns a list of values.

    Parameters
    ----------
    lst : list
        a list-like object containing sublists of numerical values.
    func: Callable
        a function that takes as an argument a list and returns a float.

    Returns
    -------
    list[float]
        a list of values that are the result of applying the func to the element.
    """
    return [func(sublist) if not sublist.empty else 0 for sublist in lst]
