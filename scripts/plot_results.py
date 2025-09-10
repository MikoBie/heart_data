"""Plot the results from all cities (hopefully)."""

# %%
from heart import PROC, PNG
import pandas as pd
from heart.plots import (
    plot_barplot,
    plot_radar,
    plot_comparison_barplots,
    plot_barhplot,
    plot_sex_barhplot,
    ticker,
)
from collections import defaultdict
from heart.radar import radar_factory
from scipy.stats import sem
from heart.utils import prepare_data


# %%
## LIVABILITY
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

belgrade["31 Do you have access in your neighbourghood to the following services?"] = (
    belgrade[
        "31 Do you have access in your neighbourghood to the following services?"
    ].apply(
        lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
    )
)

# %%
belgrade["2 How do you usually get to the demo site?"] = (
    belgrade["2 How do you usually get to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Walk", "Soft mobility", "Public transport", "Car", "Combination"],
        ordered=True,
    )
)

belgrade["3 How long does it take to get to the demo site?"] = (
    belgrade["3 How long does it take to get to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        [
            "1-10 minutes",
            "11-15 minutes",
            "16-30 minutes",
            "31-60 minutes",
            "61-120 minutes",
        ],
        ordered=True,
    )
)

belgrade["4 When do you usually visit the demo site?"] = (
    belgrade["4 When do you usually visit the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Weekdays", "Weekend", "Both"],
        ordered=True,
    )
)

belgrade["5.1 How often do you usually visit the demo site? -- Winter"] = (
    belgrade["5.1 How often do you usually visit the demo site? -- Winter"]
    .astype("category")
    .cat.reorder_categories(
        ["A few times a week", "Once a week", "Once a month", "Other"],
        ordered=True,
    )
)

belgrade["5.2 How often do you usually visit the demo site? -- Spring"] = (
    belgrade["5.2 How often do you usually visit the demo site? -- Spring"]
    .astype("category")
    .cat.reorder_categories(
        ["A few times a week", "Once a week", "Once a month", "Other"],
        ordered=True,
    )
)

belgrade["5.3 How often do you usually visit the demo site? -- Summer"] = (
    belgrade["5.3 How often do you usually visit the demo site? -- Summer"]
    .astype("category")
    .cat.reorder_categories(
        ["Everyday", "A few times a week", "Once a week", "Once a month"],
        ordered=True,
    )
)

belgrade["5.4 How often do you usually visit the demo site? -- Autumn"] = (
    belgrade["5.4 How often do you usually visit the demo site? -- Autumn"]
    .astype("category")
    .cat.reorder_categories(
        ["A few times a week", "Once a week", "Once a month", "Other"],
        ordered=True,
    )
)

belgrade[
    "6.1 What time during the day do you usually visit the demo site? -- Winter"
] = (
    belgrade[
        "6.1 What time during the day do you usually visit the demo site? -- Winter"
    ]
    .astype("category")
    .cat.reorder_categories(
        ["Morning", "Midday", "Afternoon", "Evening", "I don't visit"],
        ordered=True,
    )
)

belgrade[
    "6.2 What time during the day do you usually visit the demo site? -- Spring"
] = (
    belgrade[
        "6.2 What time during the day do you usually visit the demo site? -- Spring"
    ]
    .astype("category")
    .cat.reorder_categories(
        ["Morning", "Midday", "Afternoon", "Evening", "I don't visit"],
        ordered=True,
    )
)

belgrade[
    "6.3 What time during the day do you usually visit the demo site? -- Summer"
] = (
    belgrade[
        "6.3 What time during the day do you usually visit the demo site? -- Summer"
    ]
    .astype("category")
    .cat.reorder_categories(
        ["Morning", "Midday", "Afternoon", "Evening"],
        ordered=True,
    )
)

belgrade[
    "6.4 What time during the day do you usually visit the demo site? -- Autumn"
] = (
    belgrade[
        "6.4 What time during the day do you usually visit the demo site? -- Autumn"
    ]
    .astype("category")
    .cat.reorder_categories(
        ["Morning", "Midday", "Afternoon", "Evening", "I don't visit"],
        ordered=True,
    )
)

belgrade["7 What do you usally do during the visits to the demo site?"] = (
    belgrade["7 What do you usally do during the visits to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Sit", "Walk", "Cycle", "Use open gym", "Other"],
        ordered=True,
    )
)

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

# %%
## FIRST VISIT
## 31 Do you have access in your neighbourghood to the following services?
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = prepare_data(df=tdf, column=93).fillna(0)
    fig = plot_sex_barhplot(
        df=gdf,
        male_n=tdf.query("`19 Sex` == 'Male'")["19 Sex"].count(),
        female_n=tdf.query("`19 Sex` == 'Female'")["19 Sex"].count(),
        other_n=tdf.query("`19 Sex` == 'Prefer not to say'")["19 Sex"].count(),
    )
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")
    fig.legend(
        ncol=2, loc="center", bbox_to_anchor=(0.6, -0.03), fancybox=True, shadow=True
    )

# %%
## FINAL VISIT
## 31 Do you have access in your neighbourghood to the following services? -- nothing here
gdf = prepare_data(df=belgrade.query("version == 'final'"), column=93).fillna(0)
fig = plot_sex_barhplot(
    df=gdf,
    male_n=belgrade.query("version == 'final'")
    .query("`19 Sex` == 'Male'")["19 Sex"]
    .count(),
    female_n=belgrade.query("version == 'final'")
    .query("`19 Sex` == 'Female'")["19 Sex"]
    .count(),
    other_n=belgrade.query("version == 'final'")
    .query("`19 Sex` == 'Prefer not to say'")["19 Sex"]
    .count(),
)
fig.suptitle("Ada Ciganlija -- final visit", fontsize=12, weight="bold")
fig.legend(
    ncol=2, loc="center", bbox_to_anchor=(0.6, -0.03), fancybox=True, shadow=True
)


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

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
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
)

fig = plot_barplot(gdf, font_size=9, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
# %%
## FIRST VISIT
## How long does it take to get to the demo site?

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")["3 How long does it take to get to the demo site?"]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=9, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## How long does it take to get to the demo site?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["3 How long does it take to get to the demo site?"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=9, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## When do you usually visit the demo site?

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")["4 When do you usually visit the demo site?"]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=9, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## When do you usually visit the demo site?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["4 When do you usually visit the demo site?"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=9, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## How often do you usually visit the demo site? -- Winter

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "5.1 How often do you usually visit the demo site? -- Winter"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## How often do you usually visit the demo site? -- Winter
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["5.1 How often do you usually visit the demo site? -- Winter"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=7, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## How often do you usually visit the demo site? -- Spring

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "5.2 How often do you usually visit the demo site? -- Spring"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## How often do you usually visit the demo site? -- Spring
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["5.2 How often do you usually visit the demo site? -- Spring"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=7, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")
# %%
## FIRST VISIT
## How often do you usually visit the demo site? -- Summer

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "5.3 How often do you usually visit the demo site? -- Summer"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## How often do you usually visit the demo site? -- Summer
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["5.3 How often do you usually visit the demo site? -- Summer"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=7, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## How often do you usually visit the demo site? -- Autumn

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "5.4 How often do you usually visit the demo site? -- Autumn"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## How often do you usually visit the demo site? -- Autumn
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["5.4 How often do you usually visit the demo site? -- Autumn"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=7, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## What time do you usually visti the site? -- Winter

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "6.1 What time during the day do you usually visit the demo site? -- Winter"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## What time do you usually visti the site? -- Winter
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")[
        "6.1 What time during the day do you usually visit the demo site? -- Winter"
    ]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=8, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## What time do you usually visti the site? -- Spring

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "6.2 What time during the day do you usually visit the demo site? -- Spring"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## What time do you usually visti the site? -- Spring
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")[
        "6.2 What time during the day do you usually visit the demo site? -- Spring"
    ]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=8, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## What time do you usually visti the site? -- Summer

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "6.3 What time during the day do you usually visit the demo site? -- Summer"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## What time do you usually visti the site? -- Summer
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")[
        "6.3 What time during the day do you usually visit the demo site? -- Summer"
    ]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=8, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## What time do you usually visti the site? -- Autumn

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "6.4 What time during the day do you usually visit the demo site? -- Autumn"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## What time do you usually visti the site? -- Autumn
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")[
        "6.4 What time during the day do you usually visit the demo site? -- Autumn"
    ]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=8, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## What time do you usually visit the site? -- Autumn

for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "7 What do you usally do during the visits to the demo site?"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## They all visited Ada Ciganlija
## What time do you usually visti the site? -- Autumn
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")["7 What do you usally do during the visits to the demo site?"]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf, font_size=8, wrap_length=11)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

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
## During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?
gdf = (
    belgrade.groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
            "mean",
        ),
        std=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
            lambda x: sem(x, nan_policy="omit"),
        ),
        count=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=7.5)

# %%
## Only Ada Ciganlija
## During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
            "mean",
        ),
        std=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
            lambda x: sem(x, nan_policy="omit"),
        ),
        count=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=7.5)
fig.suptitle(
    t="Vigorous activities (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## ALL
## How much time did you usually spend doing vigorous physical acitivities on one of those days?
gdf = (
    belgrade.loc[belgrade.iloc[:, 102].apply(lambda x: not isinstance(x, str)), :]
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "40 How much time did you usually spend doing vigorous physical acitivities on one of those days?",
            "mean",
        ),
        std=(
            "40 How much time did you usually spend doing vigorous physical acitivities on one of those days?",
            lambda x: sem(x, nan_policy="omit"),
        ),
        count=(
            "40 How much time did you usually spend doing vigorous physical acitivities on one of those days?",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=160)

# %%
## Only Ada Ciganlija
## During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
            "mean",
        ),
        std=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
            lambda x: sem(x, nan_policy="omit"),
        ),
        count=(
            "39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=7.5)
fig.suptitle(
    t="Vigorous activities (Ada Ciganlija) -- comparison",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)
# %%
