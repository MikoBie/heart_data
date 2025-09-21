"""Plot the results from Athens: demographics site visits questions"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import (
    plot_barplot,
    plot_barhplot,
    ticker,
)
from clean_answers import clean_answer
import numpy as np

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

colors = {"first": "blue", "final": "green"}
# %%
## Set levels to categories
athens["version"] = (
    athens["version"]
    .astype("category")
    .cat.reorder_categories(["first", "final"], ordered=True)
)

athens["21 Martial status"] = (
    athens["21 Martial status"]
    .astype("category")
    .cat.reorder_categories(
        [
            "Single",
            "Married (including a marriage/common-law union)",
            "Divorced",
            "Widow/er",
        ]
    )
)

athens["22 Education level"] = (
    athens["22 Education level"]
    .astype("category")
    .cat.reorder_categories(
        [
            "Prefer not to say",
            "Elementary school",
            "High school",
            "Trade/technical/vocational training",
            "Commercial/technical/vocational training",
            "Bachelor's degree",
            "Master's degree",
            "PhD",
        ]
    )
)

athens["23 Occupation"] = (
    athens["23 Occupation"]
    .astype("category")
    .cat.reorder_categories(
        [
            "Prefer not to say",
            "Homemaker/unpaid career",
            "Working part time",
            "Working full time",
            "Retired but active",
            "Retired and not active",
        ]
    )
)

athens["28 What is the average total income of your household?"] = (
    athens["28 What is the average total income of your household?"]
    .map(
        lambda x: clean_answer(
            x,
            {
                "1": "Less than 5000 euros",
                "2": "Between 5000 and 10000 euros",
                "No": np.nan,
                "14": np.nan,
                "40": np.nan,
            },
        )
    )
    .astype("category")
    .cat.reorder_categories(["Less than 5000 euros", "Between 5000 and 10000 euros"])
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
## Gender
for _, tdf in athens.groupby("version"):
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
for _, tdf in athens.groupby("version"):
    gdf = tdf.groupby("19 Sex")["21 Martial status"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=15)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## Education level
for _, tdf in athens.groupby("version"):
    gdf = tdf.groupby("19 Sex")["22 Education level"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=5, wrap_length=10)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## Occupation
for _, tdf in athens.groupby("version"):
    gdf = tdf.groupby("19 Sex")["23 Occupation"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=6, wrap_length=10, perc_size=7)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What is the number of members of your household?
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["24 What is the number of members of your household?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12, perc_size=9)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What is the number people under 18 in your household?
for _, tdf in athens.groupby("version"):
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
for _, tdf in athens.groupby("version"):
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
for _, tdf in athens.groupby("version"):
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
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["28 What is the average total income of your household?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=20)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## Are you a member of any of the following groups below?
for _, tdf in athens.groupby("version"):
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
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["30 Which religious group do you belong to?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
