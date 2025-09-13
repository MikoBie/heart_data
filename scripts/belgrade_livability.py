"""Plot the results from Belgrade: LIVABILITY"""

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
belgrade = pd.read_excel(PROC / "belgrade_cleaned.xlsx")
belgrade = belgrade.rename(
    columns={
        " Please choose the park you are going to visit in the next three months": "park_planned",
        " Please choose the park you have visited in the last three months": "park_visited",
    }
)

# %%
## Demographics
belgrade.groupby(["version", "19 Sex", "1 Have you ever visited the demo site?"]).agg(
    {
        "version": "value_counts",
        "19 Sex": "value_counts",
        "18 Age": ["min", "max", "mean", "median", "std"],
        "1 Have you ever visited the demo site?": "value_counts",
    }
).reset_index()

# %%
## LIVABILITY
## FIRST VISIT
distnace = {
    "Friendliness": [0, 0.1],
    "Attractiveness": [0, -0.05],
    "Sense of\n safety": [0, 0.05],
    "Quality of\n experience": [0, -0.05],
    "Place\n attachment": [0, 0],
    "Social\n cohesion": [0, -0.03],
}
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    belgrade_all = defaultdict(lambda: defaultdict(defaultdict))

    for key, value in LIVABILITY.items():
        belgrade_all[""]["first"][key] = tdf.loc[:, value]

    theta = radar_factory(len(LIVABILITY), frame="polygon")
    fig = plot_radar(
        dt_ord=belgrade_all,
        theta=theta,
        plot_between=True,
        std=False,
        distance=distnace,
    )
    fig.suptitle(
        t=f"Belgrade {_} -- first visit",
        horizontalalignment="center",
        y=0.85,
        color="black",
        weight="bold",
        size="large",
    )
    fig.tight_layout()

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
belgrade_all = defaultdict(lambda: defaultdict(defaultdict))

for _, tdf in belgrade.groupby("version"):
    for key, value in LIVABILITY.items():
        if _ == "final":
            belgrade_all[""]["final"][key] = tdf.loc[:, value]
        else:
            belgrade_all[""]["first"][key] = tdf.query(
                "park_planned == 'Ada Ciganlija'"
            ).loc[:, value]

theta = radar_factory(len(LIVABILITY), frame="polygon")
fig = plot_radar(
    dt_ord=belgrade_all, theta=theta, plot_between=True, std=False, distance=distnace
)
fig.suptitle(
    t="Livability (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=0.85,
    color="black",
    weight="bold",
    size="large",
)
fig.savefig(PNG / "livability.png", dpi=200, bbox_inches="tight")
