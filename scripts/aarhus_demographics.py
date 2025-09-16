"""Plot the results from Aarhus: demographics site visits questions"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import (
    plot_barplot,
    plot_barhplot,
    plot_comparison_barplots,
    ticker,
)
from scipy.stats import sem

# %%
## Read data
aarhus = pd.read_excel(PROC / "aarhus_cleaned.xlsx")
aarhus = aarhus.rename(
    columns={
        " Please choose the park you are going to visit in the next three months": "park_planned",
        " Please choose the park you have visited in the last three months": "park_visited",
    }
)

aarhus = aarhus.map(
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

colors = {"first": "blue", "final": "green"}
# %%
## Set levels to categories
aarhus["version"] = (
    aarhus["version"]
    .astype("category")
    .cat.reorder_categories(["first", "final"], ordered=True)
)

aarhus["21 Martial status"] = (
    aarhus["21 Martial status"]
    .astype("category")
    .cat.reorder_categories(
        [
            "Single",
            "Married (including a marriage/common-law union)",
            "Divorced",
        ]
    )
)

aarhus["22 Education level"] = (
    aarhus["22 Education level"]
    .astype("category")
    .cat.reorder_categories(
        [
            "Prefer not to say",
            "Elementary school",
            "High school",
            "Trade/technical/vocational training",
            "Bachelor's degree",
            "Master's degree",
            "PhD",
        ]
    )
)

aarhus["23 Occupation"] = (
    aarhus["23 Occupation"]
    .astype("category")
    .cat.reorder_categories(
        [
            "Unemployed",
            "Student",
            "Working part time",
            "Working full time",
            "Retired but active",
            "Retired and not active",
        ]
    )
)

# %%
## Demographics
aarhus.groupby(["version", "19 Sex", "1 Have you ever visited the demo site?"]).agg(
    {
        "version": "value_counts",
        "19 Sex": "value_counts",
        "18 Age": ["min", "max", "mean", "median", "std"],
        "1 Have you ever visited the demo site?": "value_counts",
    }
).reset_index()

# %%
## Gender
for _, tdf in aarhus.groupby("version"):
    gdf = tdf["20 Gender"].value_counts().reset_index()
    fig = plot_barhplot(
        df=gdf,
        x="20 Gender",
        y="count",
        percenteges=True,
        labels=False,
        color=colors[_],
    )
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## Martial status
for _, tdf in aarhus.groupby("version"):
    gdf = tdf.groupby("19 Sex")["21 Martial status"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## Education level
for _, tdf in aarhus.groupby("version"):
    gdf = tdf.groupby("19 Sex")["22 Education level"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=5, wrap_length=10)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## Occupation
for _, tdf in aarhus.groupby("version"):
    gdf = tdf.groupby("19 Sex")["23 Occupation"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What is the number of members of your household?
for _, tdf in aarhus.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["24 What is the number of members of your household?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What is the number people under 18 in your household?
for _, tdf in aarhus.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "25 What is the number of people under 18 in your household?"
        ]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## How many children under 5 you have?
for _, tdf in aarhus.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["26 How many children under 5 you have?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What is the number of members of your household contributing to the household budget?
for _, tdf in aarhus.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "27 What is the number of members of your household contributing to the household budget?"
        ]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What is the average total income of your household?
gdf = (
    aarhus.groupby(["19 Sex", "version"])
    .agg(
        mean=("28 What is the average total income of your household?", "mean"),
        std=("28 What is the average total income of your household?", sem),
        count=("28 What is the average total income of your household?", "count"),
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

fig = plot_comparison_barplots(gdf=gdf, max_value=1300000)

# %%
## Are you a member of any of the following groups below?
for _, tdf in aarhus.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "29 Are you a member of any of the following groups below?"
        ]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## Which religious group do you belong to?
for _, tdf in aarhus.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["30 Which religious group do you belong to?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
