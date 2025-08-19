"""
Compute some basic statistics.
"""

# %%
from heart import PROC
import pandas as pd

# %%
athens = pd.read_excel(PROC / "Athens.xlsx")
aarhus = pd.read_excel(PROC / "Aarhus.xlsx")
belgrade = pd.read_excel(PROC / "Belgrade.xlsx")

# %%
## Demographics
print(aarhus.groupby("version")["city"].value_counts())
print(belgrade.groupby("version")["city"].value_counts())
print(athens.groupby("version")["city"].value_counts())

# %%
aarhus.groupby(["version", "19 Sex"]).agg(
    sex_count=pd.NamedAgg(column="18 Age", aggfunc="count")
).reset_index()
# %%
belgrade.groupby(["version", "19 Sex"]).agg(
    sex_count=pd.NamedAgg(column="18 Age", aggfunc="count")
).reset_index()
# %%
athens.groupby(["version", "19 Sex"]).agg(
    sex_count=pd.NamedAgg(column="18 Age", aggfunc="count")
).reset_index()

# %%
