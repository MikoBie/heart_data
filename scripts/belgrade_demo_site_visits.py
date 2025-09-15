"""Plot the results from Belgrade: demo site visits questions"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import (
    plot_barplot,
    plot_sex_barhplot,
)
from heart.utils import prepare_data

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

belgrade["31 Do you have access in your neighbourghood to the following services?"] = (
    belgrade[
        "31 Do you have access in your neighbourghood to the following services?"
    ].apply(
        lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
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
