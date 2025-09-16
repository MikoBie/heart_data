"""Plot the results from Athens: psychological questions"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import (
    plot_comparison_barplots,
)
from scipy.stats import sem


# %%
## Read data
athens = pd.read_excel(PROC / "athens_cleaned.xlsx")
athens = athens.rename(
    columns={
        " Please choose the park you are going to visit in the next three months": "park_planned",
        " Please choose the park you have visited in the last three months": "park_visited",
    }
)

athens = athens.map(
    lambda x: {
        "Bicycle, ,scooter, etc.": "Soft mobility",
        "Combination of the above": "Combination",
        "Morning (6-10)": "Morning",
        "Midday (10-14)": "Midday",
        "Afternoon (14-18)": "Afternoon",
        "Evening (18-22)": "Evening",
        "Night (22-6)": "Night",
        "predominantly walk": "Walk",
        "predominantly sit": "Sit",
        "mostly cycle": "Cycle",
        "mostly use open gym": "Use open gym",
    }.get(x, x)
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
## Satisfaction With Life Scale
gdf = (
    athens.groupby(["19 Sex", "version"])
    .agg(
        mean=("swls", "mean"),
        std=("swls", sem),
        count=("swls", "count"),
    )
    .reset_index()
)

gdf["version"] = (
    gdf["version"]
    .astype("category")
    .cat.reorder_categories(
        ["first", "final"],
        ordered=True,
    )
)

fig = plot_comparison_barplots(gdf=gdf, max_value=35)

# %%
## Warwick wellbeing
gdf = (
    athens.groupby(["19 Sex", "version"])
    .agg(
        mean=("warwick_wellbeing", "mean"),
        std=("warwick_wellbeing", sem),
        count=("warwick_wellbeing", "count"),
    )
    .reset_index()
)

gdf["version"] = (
    gdf["version"]
    .astype("category")
    .cat.reorder_categories(
        ["first", "final"],
        ordered=True,
    )
)

fig = plot_comparison_barplots(gdf=gdf, max_value=35)

# %%
## UCLA loneliness
gdf = (
    athens.groupby(["19 Sex", "version"])
    .agg(
        mean=("ucla_loneliness", "mean"),
        std=("ucla_loneliness", sem),
        count=("ucla_loneliness", "count"),
    )
    .reset_index()
)

gdf["version"] = (
    gdf["version"]
    .astype("category")
    .cat.reorder_categories(
        ["first", "final"],
        ordered=True,
    )
)

fig = plot_comparison_barplots(gdf=gdf, max_value=9)

# %%
## ALL
## DAAS Depresion scale
gdf = (
    athens.groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_depression",
            "mean",
        ),
        std=(
            "dass_depression",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_depression",
            "count",
        ),
    )
    .reset_index()
)

gdf["version"] = (
    gdf["version"]
    .astype("category")
    .cat.reorder_categories(
        ["first", "final"],
        ordered=True,
    )
)

fig = plot_comparison_barplots(gdf=gdf, max_value=54)
fig.axes[0].set_ylabel("Depression")

# %%
## DAAS Anxiety scale
gdf = (
    athens.groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_anxiety",
            "mean",
        ),
        std=(
            "dass_anxiety",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_anxiety",
            "count",
        ),
    )
    .reset_index()
)

gdf["version"] = (
    gdf["version"]
    .astype("category")
    .cat.reorder_categories(
        ["first", "final"],
        ordered=True,
    )
)

fig = plot_comparison_barplots(gdf=gdf, max_value=54)
fig.axes[0].set_ylabel("Anxiety")

# %%
## DAAS Stress scale
gdf = (
    athens.groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_stress",
            "mean",
        ),
        std=(
            "dass_stress",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_stress",
            "count",
        ),
    )
    .reset_index()
)

gdf["version"] = (
    gdf["version"]
    .astype("category")
    .cat.reorder_categories(
        ["first", "final"],
        ordered=True,
    )
)

fig = plot_comparison_barplots(gdf=gdf, max_value=54)
fig.axes[0].set_ylabel("Stress")
