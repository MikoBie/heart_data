"""Script to clean and translate answers for local languages."""

# %%
import pandas as pd
from heart import PROC
from heart.mappings import aarhus_a_dct, belgrade_a_dct, athens_a_dct

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
        df = translate_answers(df=df, mappings=mapping)
        df.to_excel(PROC / f"{key}_cleaned.xlsx", index=False)


# %%
if __name__ == "__main__":
    main()

# %%
