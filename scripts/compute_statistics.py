# %%
from heart import PROC
from heart.mappings import questionnaire_first
import pandas as pd

# %%
athens = pd.read_excel(PROC / "Athens.xlsx")
aarhus = pd.read_excel(PROC / "Aarhus.xlsx")
belgrade = pd.read_excel(PROC / "Belgrade.xlsx")

dct = {value: key for key, value in questionnaire_first.items()}

# %%
lst = []
with open("athens.txt", "w") as file:
    for line in athens.columns.tolist():
        if line in dct:
            lst.append(dct[line])
        else:
            file.write(line + "\n")


# %%
lst_srtd = sorted([float(item) for item in lst])

# %%
len(lst_srtd)

# %%
