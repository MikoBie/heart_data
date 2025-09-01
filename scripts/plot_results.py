"""Plot the results from all cities (hopefully)."""

# %%
from heart import PROC
import pandas as pd
from heart.plots import plot_barplot


# %%
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
## Plans vs reality
belgrade.agg(
    {
        "park_planned": "value_counts",
        "park_visited": "value_counts",
    }
)
# %%
## FIRST VISIT
## How do you usually get to the demo site?
temp = belgrade.query("version == 'first'").map(
    lambda x: {
        "Bicycle, ,scooter, etc.": "Soft mobility",
        "Combination of the above": "Combination",
    }.get(x, x)
)
temp["2 How do you usually get to the demo site?"] = (
    temp["2 How do you usually get to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Walk", "Soft mobility", "Public transport", "Car", "Combination"],
        ordered=True,
    )
)

for _, tdf in temp.groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")["2 How do you usually get to the demo site?"]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=9, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## How do you usually get to the demo site?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["2 How do you usually get to the demo site?"]
    .value_counts()
    .reset_index()
    .map(
        lambda x: {
            "Bicycle, ,scooter, etc.": "Soft mobility",
            "Combination of the above": "Combination",
        }.get(x, x)
    )
)

gdf["2 How do you usually get to the demo site?"] = (
    gdf["2 How do you usually get to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Walk", "Soft mobility", "Car", "Combination"], ordered=True
    )
)

fig = plot_barplot(gdf)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## How do you usually get to the demo site?
temp = belgrade.query("version == 'first'").map(
    lambda x: {
        "Bicycle, ,scooter, etc.": "Soft mobility",
        "Combination of the above": "Combination",
    }.get(x, x)
)
temp["3 How long does it take to get to the demo site?"] = (
    temp["3 How long does it take to get to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Walk", "Soft mobility", "Public transport", "Car", "Combination"],
        ordered=True,
    )
)

for _, tdf in temp.groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")["2 How do you usually get to the demo site?"]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=9, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## How do you usually get to the demo site?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["2 How do you usually get to the demo site?"]
    .value_counts()
    .reset_index()
    .map(
        lambda x: {
            "Bicycle, ,scooter, etc.": "Soft mobility",
            "Combination of the above": "Combination",
        }.get(x, x)
    )
)

gdf["2 How do you usually get to the demo site?"] = (
    gdf["2 How do you usually get to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Walk", "Soft mobility", "Car", "Combination"], ordered=True
    )
)

fig = plot_barplot(gdf)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")
