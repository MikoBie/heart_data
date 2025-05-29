# %%
from heart import PROC
from heart.mappings import (
    questionnaire_first,
    belgrade_q_dct,
    athens_q_dct,
    aarhus_q_dct,
)
import pandas as pd
from collections import defaultdict

# %%
athens = pd.read_excel(PROC / "Athens.xlsx")
aarhus = pd.read_excel(PROC / "Aarhus.xlsx")
belgrade = pd.read_excel(PROC / "Belgrade.xlsx")

lst_srcs = [athens, aarhus, belgrade]

questionnaire_first_reversed = {
    value: key for key, value in questionnaire_first.items()
}
belgrade_q_dct_reversed = {value: key for key, value in belgrade_q_dct.items()}
athens_q_dct_reversed = {value: key for key, value in athens_q_dct.items()}
aarhus_q_dct_reversed = {value: key for key, value in aarhus_q_dct.items()}


backtranslate_dct = {
    "Aarhus": aarhus_q_dct_reversed,
    "Belgrade": belgrade_q_dct_reversed,
    "Athens": athens_q_dct_reversed,
}

# %%
dct = defaultdict(dict)
for df in lst_srcs:
    for col in df.columns[5:]:
        if col not in questionnaire_first_reversed:
            dct[df.city[0]][backtranslate_dct[df.city[0]][col]] = col
