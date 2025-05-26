# %%
from heart import BIO, PROC
from heart.utils import date_quarter
import pandas as pd
from tqdm import tqdm
import os
import re

# %%
lst_athens = [item for item in os.scandir(BIO / "athens") if "xlsx" in item.name]
lst_aarhus = [item for item in os.scandir(BIO / "aarhus") if "xlsx" in item.name]
lst_belgrade = [item for item in os.scandir(BIO / "belgrade") if "xlsx" in item.name]
rgx_dt = re.compile(r"\d{4}-\d{2}")


# %%
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


def explode_rows(df: pd.DataFrame, n_doubles: int = 50) -> pd.DataFrame:
    """Explode the rows of a data frame. By default, explodes the rows with more
    than 50 columns witt lists as values. If the row has less than 50 columns
    with lists it returns the last element from the list.

    Parameters
    ----------
    df : pd.DataFrame
        a data frame in wide format.
    n_doubles : int, optional
        the number of columns in the row with lists (this indicates the final questionnaire written
        as first questionnaire), by default 50

    Returns
    -------
    pd.DataFrame
        a data frame with exploded rows.
    """
    questionnaire = pd.DataFrame()
    for _, item in tqdm(df.reset_index().map(lambda x: isinstance(x, list)).iterrows()):
        if sum(item) > n_doubles:
            tmp = (
                df.reset_index()
                .query(f"index == {_}")
                .explode(item.index[item].tolist())
            )
            tmp["version"] = ["first", "final"]
        else:
            tmp = df.reset_index().query(f"index == {_}")
            tmp = tmp.map(
                lambda x: extract_first_element(x[::-1]) if isinstance(x, list) else x
            )
        questionnaire = pd.concat([questionnaire, tmp])

    return questionnaire


def wide_excel(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the excel in long format to wide format.

    Parameters
    ----------
    df : pd.DataFrame
        a data frame in long format

    Returns
    -------
    pd.DataFrame
        a data frame in wide format
    """
    df["date_simple"] = df["created_at"].apply(lambda x: date_quarter(x))
    df = df[
        [
            "user_id",
            "date_simple",
            "city",
            "version",
            "question_eng",
            "response",
            "questionTitle",
        ]
    ]
    return df.pivot(
        index=["user_id", "date_simple", "version", "city"],
        columns="question_eng",
        values="response",
    )


def merge_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Merge rows with the same user_id, version, and city.

    Parameters
    ----------
    df : pd.DataFrame
        a data frame in wide format

    Returns
    -------
    pd.DataFrame
        a data frame with merged rows
    """
    df = (
        df.sort_values("date_simple", ascending=True)
        .groupby(["user_id", "version", "city"], as_index=True)
        .agg(lambda x: list(x.dropna()))
        .map(lambda x: extract_first_element(x) if len(x) < 2 else x[-2:])
    )
    return df


def merge_excells(
    lst_fls: list,
) -> None:
    """Merge multiple excells into one excell in long format.

    Parameters
    ----------
    lst_fls : list
        a list of DirEntries fo Excel files.
    """
    questionnaire = pd.DataFrame()
    for item in tqdm(lst_fls):
        tmp = pd.read_excel(item)
        questionnaire = pd.concat([questionnaire, tmp])

    city = questionnaire["city"].unique()[0]
    file_name = f"{city}.xlsx"
    questionnaire = wide_excel(df=questionnaire)
    questionnaire = merge_rows(df=questionnaire)
    questionnaire
    questionnaire = explode_rows(df=questionnaire)
    questionnaire.reset_index().to_excel(PROC / file_name)


def main() -> None:
    print("Process data from Athens")
    merge_excells(lst_athens)
    print("Process data from Aarhus")
    merge_excells(lst_aarhus)
    print("Process data from Belgrade")
    merge_excells(lst_belgrade)


# %%
if __name__ in "__main__":
    df = main()

# %%
