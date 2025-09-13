"""Plot the results from Belgrade: demographics site visits questions"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import (
    plot_barplot,
    plot_comparison_barplots,
    plot_barhplot,
    ticker,
)
from scipy.stats import sem

# %%
## Read data
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
## Set levels to categories
belgrade["21 Martial status"] = (
    belgrade["21 Martial status"]
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

belgrade["22 Education level"] = (
    belgrade["22 Education level"]
    .astype("category")
    .cat.reorder_categories(
        [
            "Prefer not to say",
            "High school",
            "Trade/technical/vocational training",
            "Bachelor's degree",
            "Master's degree",
            "PhD",
        ]
    )
)

belgrade["23 Occupation"] = (
    belgrade["23 Occupation"]
    .astype("category")
    .cat.reorder_categories(
        [
            "Student",
            "Working full time",
            "Retired but active",
            "Retired and not active",
            "Unemployed",
        ]
    )
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
## FIRST VISIT
## Gender
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = tdf["20 Gender"].value_counts().reset_index()
    fig = plot_barhplot(
        df=gdf, x="20 Gender", y="count", percenteges=True, labels=False
    )
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## Gender
gdf = belgrade.query("version == 'final'")["20 Gender"].value_counts().reset_index()

fig = plot_barhplot(
    df=gdf, x="20 Gender", y="count", percenteges=True, labels=False, color="green"
)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## Martial status
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = tdf.groupby("19 Sex")["21 Martial status"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## Martial status
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["21 Martial status"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=12)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## Education level
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = tdf.groupby("19 Sex")["22 Education level"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## Education level
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["22 Education level"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=12)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## Occupation
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = tdf.groupby("19 Sex")["23 Occupation"].value_counts().reset_index()
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## Occupation
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["23 Occupation"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=13)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## What is the number of members of your household?
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")["24 What is the number of members of your household?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## What is the number of members of your household?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["24 What is the number of members of your household?"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=13)
fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## What is the number people under 18 in your household?
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "25 What is the number of people under 18 in your household?"
        ]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## What is the number of people under 18 in your household?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["25 What is the number of people under 18 in your household?"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=13)
fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## How many children under 5 you have?
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")["26 How many children under 5 you have?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## How many children under 5 you have?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["26 How many children under 5 you have?"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=13)
fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## What is the number of members of your household contributing to the household budget?
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "27 What is the number of members of your household contributing to the household budget?"
        ]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## What is the number of members of your household contributing to the household budget?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")[
        "27 What is the number of members of your household contributing to the household budget?"
    ]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=13)
fig.axes[0].xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: int(x)))
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## ALL
## What is the average total income of your household?
gdf = (
    belgrade.groupby(["19 Sex", "version"])
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

fig = plot_comparison_barplots(gdf=gdf, max_value=200000)

# %%
## Only Ada Ciganlija
## What is the average total income of your household?
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
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

fig = plot_comparison_barplots(gdf=gdf, max_value=200000)
fig.suptitle(
    t="Loneliness (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## FIRST VISIT
## Are you a member of any of the following groups below? -- There is nothing here
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "29 Are you a member of any of the following groups below?"
        ]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## Are you a member of any of the following groups below? -- There is nothing here
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["29 Are you a member of any of the following groups below?"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=13)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## Which religious group do you belong to?
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")["30 Which religious group do you belong to?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=12)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## Are you a member of any of the following groups below? -- There is nothing here
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["30 Which religious group do you belong to?"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=13)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")
