"""Script to clean and translate answers for local languages."""

# %%
import pandas as pd
from heart import PROC
from heart.mappings import aarhus_a_dct, belgrade_a_dct, athens_a_dct
from typing import Any

# %%
athens = pd.read_excel(PROC / "Athens.xlsx")
belgrade = pd.read_excel(PROC / "Belgrade.xlsx")
aarhus = pd.read_excel(PROC / "Aarhus.xlsx")

dct_df = {
    "Athens": {"df": athens, "mapping": athens_a_dct},
    "Belgrade": {"df": belgrade, "mapping": belgrade_a_dct},
    "Aarhus": {"df": aarhus, "mapping": aarhus_a_dct},
}


# %%
def translate_answers(df: pd.DataFrame, mappings: dict) -> pd.DataFrame:
    """
    Translates answers int the data frame from local languages to English.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the answers to be translated.
    mappings : dict
        Dictionary containing the mappings for translation.

    Returns:
    --------
    pd.DataFrame
        DataFrame with translated answers.
    """
    return df.map(lambda x: mappings.get(x, x) if isinstance(x, str) else x)


def split_string(s: str) -> list:
    """
    Splits a string by commas and strips whitespace.

    Parameters:
    -----------
    s : str
        Input string to be split.

    Returns:
    --------
    list
        List of cleaned strings.
    """
    if not isinstance(s, str):
        return []
    return [item.strip() for item in s.split(",")]


def clean_answer(el: Any, mapping: dict) -> str | Any:
    """
    Returns a cleaned string by stripping whitespace and converting numbers to strings. It maps the string to meanigful answers. If the input is not a string or number, it returns the input as is.

    Parameters:
    -----------
    el : Any
        Input element to be cleaned.
    mapping : dict
        Dictionary containing the mappings for translation.

    Returns:
    --------
    str|Any
        cleaned string or element as it was (if the intput was different thana a string or number).
    """
    if isinstance(el, float) and pd.notna(el):
        el = str(int(el)).strip()
    elif isinstance(el, int):
        el = str(el).strip()
    elif isinstance(el, str):
        el = el.strip()
    return mapping.get(el, el)


# %%
def main():
    """
    Main function to clean and translate answers in the datasets.
    """
    global dct_df
    for key, value in dct_df.items():
        df = value["df"]
        mapping = value["mapping"]
        df.loc[
            :, "31 Do you have access in your neighbourghood to the following services?"
        ] = df[
            "31 Do you have access in your neighbourghood to the following services?"
        ].apply(
            lambda x: "; ".join([mapping.get(item, item) for item in split_string(x)])
        )
        df.loc[:, "1 Have you ever visited the demo site?"] = (
            df.loc[:, "1 Have you ever visited the demo site?"]
            .map(lambda x: clean_answer(x, {"1": "Yes", "2": "No"}))
            .astype("object")
        )
        df.loc[:, "19 Sex"] = (
            df.loc[:, "19 Sex"]
            .map(lambda x: clean_answer(x, {"1": "Male", "2": "Female"}))
            .astype("object")
        )
        df = translate_answers(df=df, mappings=mapping)
        df.to_excel(PROC / f"{key}_cleaned.xlsx", index=False)


# %%
if __name__ == "__main__":
    main()

# %%
