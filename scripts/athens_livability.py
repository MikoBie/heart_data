"""Plot the results from Athens: LIVABILITY"""

# %%
from heart import PROC, PNG
import pandas as pd
from heart.plots import (
    plot_radar,
)
from collections import defaultdict
from heart.radar import radar_factory


# %%
## Read data
LIVABILITY = {
    "Friendliness": "friendliness",
    "Attractiveness": "attractiveness",
    "Quality of\n experience": "quality_of_experience",
    "Sense of\n safety": "sense_of_safety",
    "Place\n attachment": "place_attachment",
    "Social\n cohesion": "social_cohesion",
}
athens = pd.read_excel(PROC / "athens_cleaned.xlsx")
athens = athens.rename(
    columns={
        " Please choose the park you are going to visit in the next three months": "park_planned",
        " Please choose the park you have visited in the last three months": "park_visited",
    }
)

# %%
## Demographics -- In general, the issue is that most of the questionnaires
## is incomplete. In 80 (first -- 56; final 24) of them Sex of the participant
## is missing!?!
## There is one user_id which is in final visit and not in first visit.
athens.groupby(["version", "19 Sex", "1 Have you ever visited the demo site?"]).agg(
    {
        "version": "value_counts",
        "19 Sex": "value_counts",
        "18 Age": ["min", "max", "mean", "median", "std"],
        "1 Have you ever visited the demo site?": "value_counts",
    }
).reset_index()

# %%
## LIVABILITY
## FINAL VISIT
## Ada Ciganlija only
distnace = {
    "Friendliness": [0, 0.08],
    "Attractiveness": [0, 0],
    "Quality of\n experience": [0, -0.08],
    "Sense of\n safety": [0, -0.00],
    "Place\n attachment": [0, 0],
    "Social\n cohesion": [0, -0.01],
}
athens_all = defaultdict(lambda: defaultdict(defaultdict))

for _, tdf in athens.groupby("version"):
    for key, value in LIVABILITY.items():
        athens_all[""][_][key] = tdf.loc[:, value]

theta = radar_factory(len(LIVABILITY), frame="polygon")
fig = plot_radar(
    dt_ord=athens_all, theta=theta, plot_between=True, std=False, distance=distnace
)
fig.suptitle(
    t="Livability -- comparison",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.savefig(PNG / "livability.png", dpi=200, bbox_inches="tight")
