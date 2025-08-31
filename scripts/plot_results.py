"""Plot the results from all cities (hopefully)."""

# %%
from heart import PROC
import pandas as pd

# %%
belgrade = pd.read_excel(PROC / "belgrade_cleaned.xlsx")

# %%
belgrade.groupby(["version", "19 Sex"]).agg(
    {
        "version": "value_counts",
        "19 Sex": "value_counts",
        "18 Age": ["min", "max", "mean", "median", "std"],
    }
)
# %%
