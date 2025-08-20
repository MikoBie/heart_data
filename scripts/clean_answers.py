"""Script to clean and translate answers for local languages."""

# %%
import pandas as pd
from heart import PROC

# %%
athens = pd.read_excel(PROC / "Athens.xlsx")
belgrade = pd.read_excel(PROC / "Belgrade.xlsx")
aarhus = pd.read_excel(PROC / "Aarhus.xlsx")


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
    return df.map(mappings)


# %%
