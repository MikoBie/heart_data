"""Plot the results from Belgrade: psychological questions"""

# %%
from heart import PROC, PNG
import pandas as pd
from heart.plots import (
    plot_comparison_barplots,
)
from scipy.stats import sem


# %%
belgrade = pd.read_excel(PROC / "belgrade_cleaned.xlsx")
belgrade = belgrade.rename(
    columns={
        " Please choose the park you are going to visit in the next three months": "park_planned",
        " Please choose the park you have visited in the last three months": "park_visited",
    }
)

belgrade = belgrade.map(
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
## ALL
## Satisfaction With Life Scale
gdf = (
    belgrade.groupby(["19 Sex", "version"])
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
## Only Ada Ciganlija
## Satisfaction With Life Scale
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
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
fig.suptitle(
    t="SWLS (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1,
    color="black",
    weight="bold",
    size="large",
)
fig.savefig(PNG / "swls.png", dpi=200, bbox_inches="tight")

# %%
## ALL
## Warwick wellbeing
gdf = (
    belgrade.groupby(["19 Sex", "version"])
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
## Only Ada Ciganlija
## Warwick wellbeing
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
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
fig.suptitle(
    t="Well-being (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1,
    color="black",
    weight="bold",
    size="large",
)
fig.savefig(PNG / "wellbeing.png", dpi=200, bbox_inches="tight")
# %%
## ALL
## UCLA loneliness
gdf = (
    belgrade.groupby(["19 Sex", "version"])
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
## Only Ada Ciganlija
## UCLA loneliness
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
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
fig.suptitle(
    t="Loneliness (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)
fig.savefig(PNG / "loneliness.png", dpi=200, bbox_inches="tight")

# %%
## ALL
## DAAS Depresion scale
gdf = (
    belgrade.groupby(["19 Sex", "version"])
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
## Only Ada Ciganlija
## DASS Depression Scale
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
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
fig.suptitle(
    t="Depression (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## ALL
## DAAS Anxiety scale
gdf = (
    belgrade.groupby(["19 Sex", "version"])
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
fig.axes[0].set_ylabel("Depression")

# %%
## Only Ada Ciganlija
## Dass Anxiety Scale
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
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
fig.suptitle(
    t="Anxiety (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## ALL
## DAAS Stress scale
gdf = (
    belgrade.groupby(["19 Sex", "version"])
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

# %%
## Only Ada Ciganlija
## DASS Stress scale
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
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
fig.suptitle(
    t="Stress (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)
