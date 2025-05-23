# %%
from heart import BIO, PROC
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
    df["date_simple"] = df["created_at"].apply(lambda x: rgx_dt.search(x).group())
    df = df[["user_id", "date_simple", "city", "version", "question_eng", "response"]]
    return df.pivot(
        index=["user_id", "date_simple", "version", "city"],
        columns="question_eng",
        values="response",
    )


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
    main()
