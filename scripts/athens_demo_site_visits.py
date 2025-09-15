"""Plot the results from Athens: demo site visits questions"""

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
## Set levels to categories
athens["version"] = (
    athens["version"]
    .astype("category")
    .cat.reorder_categories(["first", "final"], ordered=True)
)

athens["2 How do you usually get to the demo site?"] = (
    athens["2 How do you usually get to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Walk", "Soft mobility", "Public transport", "Car", "Combination"],
        ordered=True,
    )
)

athens["3 How long does it take to get to the demo site?"] = (
    athens["3 How long does it take to get to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        [
            "1-10 minutes",
            "11-15 minutes",
            "16-30 minutes",
            "31-60 minutes",
            "61-120 minutes",
            "Longer than 2 hours",
        ],
        ordered=True,
    )
)

athens["4 When do you usually visit the demo site?"] = (
    athens["4 When do you usually visit the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Weekdays", "Weekend", "Both"],
        ordered=True,
    )
)

athens["5.1 How often do you usually visit the demo site? -- Winter"] = (
    athens["5.1 How often do you usually visit the demo site? -- Winter"]
    .astype("category")
    .cat.reorder_categories(
        ["Once a week", "Once a month", "I don't visit", "Other"],
        ordered=True,
    )
)

athens["5.2 How often do you usually visit the demo site? -- Spring"] = (
    athens["5.2 How often do you usually visit the demo site? -- Spring"]
    .astype("category")
    .cat.reorder_categories(
        ["A few times a week", "Once a week", "Once a month", "I don't visit", "Other"],
        ordered=True,
    )
)

athens["5.3 How often do you usually visit the demo site? -- Summer"] = (
    athens["5.3 How often do you usually visit the demo site? -- Summer"]
    .astype("category")
    .cat.reorder_categories(
        ["A few times a week", "Once a week", "Once a month", "I don't visit", "Other"],
        ordered=True,
    )
)

athens["5.4 How often do you usually visit the demo site? -- Autumn"] = (
    athens["5.4 How often do you usually visit the demo site? -- Autumn"]
    .astype("category")
    .cat.reorder_categories(
        ["A few times a week", "Once a week", "Once a month", "I don't visit", "Other"],
        ordered=True,
    )
)

athens["6.1 What time during the day do you usually visit the demo site? -- Winter"] = (
    athens["6.1 What time during the day do you usually visit the demo site? -- Winter"]
    .astype("category")
    .cat.reorder_categories(
        ["Morning", "Midday", "Afternoon", "Evening", "I don't visit"],
        ordered=True,
    )
)

athens["6.2 What time during the day do you usually visit the demo site? -- Spring"] = (
    athens["6.2 What time during the day do you usually visit the demo site? -- Spring"]
    .astype("category")
    .cat.reorder_categories(
        ["Morning", "Midday", "Afternoon", "Evening", "I don't visit"],
        ordered=True,
    )
)

athens["6.3 What time during the day do you usually visit the demo site? -- Summer"] = (
    athens["6.3 What time during the day do you usually visit the demo site? -- Summer"]
    .astype("category")
    .cat.reorder_categories(
        ["Morning", "Midday", "Afternoon", "Evening", "I don't visit"],
        ordered=True,
    )
)

athens["6.4 What time during the day do you usually visit the demo site? -- Autumn"] = (
    athens["6.4 What time during the day do you usually visit the demo site? -- Autumn"]
    .astype("category")
    .cat.reorder_categories(
        ["Morning", "Midday", "Afternoon", "Evening", "I don't visit"],
        ordered=True,
    )
)

athens["7 What do you usally do during the visits to the demo site?"] = (
    athens["7 What do you usally do during the visits to the demo site?"]
    .astype("category")
    .cat.reorder_categories(
        ["Sit", "Walk", "Cycle", "Use open gym", "Other"],
        ordered=True,
    )
)

athens["31 Do you have access in your neighbourghood to the following services?"] = (
    athens[
        "31 Do you have access in your neighbourghood to the following services?"
    ].apply(
        lambda x: [item.strip() for item in x.split(";")] if isinstance(x, str) else []
    )
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
## Have you ever visited the demo site?
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["1 Have you ever visited the demo site?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf, font_size=9, wrap_length=10)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")


# %%
## How do you usually get to the demo site?
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["2 How do you usually get to the demo site?"]
        .value_counts()
        .reset_index()
    )
    fig = plot_barplot(gdf, font_size=9, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## 31 Do you have access in your neighbourghood to the following services?
for _, tdf in athens.groupby("version"):
    gdf = prepare_data(df=tdf, column=93).fillna(0)
    fig = plot_sex_barhplot(
        df=gdf,
        male_n=tdf.query("`19 Sex` == 'Male'")["19 Sex"].count(),
        female_n=tdf.query("`19 Sex` == 'Female'")["19 Sex"].count(),
        other_n=tdf.query("`19 Sex` == 'Prefer not to say'")["19 Sex"].count(),
    )
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")
    fig.legend(
        ncol=2, loc="center", bbox_to_anchor=(0.6, -0.03), fancybox=True, shadow=True
    )

# %%
## How long does it take to get to the demo site?
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["3 How long does it take to get to the demo site?"]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=10)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")


# %%
## When do you usually visit the demo site?
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")["4 When do you usually visit the demo site?"]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=9, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## How often do you usually visit the demo site? -- Winter
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "5.1 How often do you usually visit the demo site? -- Winter"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## How often do you usually visit the demo site? -- Spring
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "5.2 How often do you usually visit the demo site? -- Spring"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=10)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## How often do you usually visit the demo site? -- Summer
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "5.3 How often do you usually visit the demo site? -- Summer"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## How often do you usually visit the demo site? -- Autumn
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "5.4 How often do you usually visit the demo site? -- Autumn"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What time do you usually visti the site? -- Winter
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "6.1 What time during the day do you usually visit the demo site? -- Winter"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What time do you usually visti the site? -- Spring
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "6.2 What time during the day do you usually visit the demo site? -- Spring"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What time do you usually visti the site? -- Summer
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "6.3 What time during the day do you usually visit the demo site? -- Summer"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What time do you usually visti the site? -- Autumn
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "6.4 What time during the day do you usually visit the demo site? -- Autumn"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## What do you usually do during the visits to the demo site?
for _, tdf in athens.groupby("version"):
    gdf = (
        tdf.groupby("19 Sex")[
            "7 What do you usally do during the visits to the demo site?"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=8, wrap_length=11)
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")
