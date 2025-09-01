"""Plot the results from all cities (hopefully)."""

# %%
from heart import PROC, PNG
import pandas as pd
from heart.plots import plot_barplot, plot_radar, plot_comparison_barplots
from collections import defaultdict
from heart.radar import radar_factory
from scipy.stats import sem


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
