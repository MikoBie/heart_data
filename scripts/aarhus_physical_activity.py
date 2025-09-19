"""Plot the results from Aarhus: Physical activity"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import (
    plot_comparison_barplots,
    plot_barhplot,
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

# %%
## Set level to categories
aarhus["version"] = (
    aarhus["version"]
    .astype("category")
    .cat.reorder_categories(["first", "final"], ordered=True)
)
# %%
## When you are working, which of the following best describes what you do?
for _, tdf in aarhus.groupby("version"):
    gdf = (
        tdf[
            "46 When you are working, which of the following best describes what you do?"
        ]
        .value_counts()
        .reset_index()
    )
    fig = plot_barhplot(
        df=gdf,
        x="46 When you are working, which of the following best describes what you do?",
        y="count",
        percenteges=True,
        labels=False,
    )
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## Do you smoke tabacco?
for _, tdf in aarhus.groupby("version"):
    gdf = tdf["47 Do you smoke tabacco?"].value_counts().reset_index()
    fig = plot_barhplot(
        df=gdf, x="47 Do you smoke tabacco?", y="count", percenteges=True, labels=False
    )
    fig.suptitle(f"{_.capitalize()} visit", fontsize=12, weight="bold")

# %%
## During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?
gdf = (
    aarhus.groupby(["19 Sex", "version"])
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
fig.axes[0].set_ylabel("Days")

# %%
## How much time did you usually spend doing vigorous physical acitivities on one of those days?
gdf = (
    aarhus.loc[aarhus.iloc[:, 102].apply(lambda x: not isinstance(x, str)), :]
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "40 How much time did you usually spend doing vigorous physical acitivities on one of those days?",
            "mean",
        ),
        std=(
            "40 How much time did you usually spend doing vigorous physical acitivities on one of those days?",
            lambda x: sem(x.astype(float), nan_policy="omit"),
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

fig = plot_comparison_barplots(gdf=gdf, max_value=250)
fig.axes[0].set_ylabel("Minutes")

# %%
## During the last 7 days, on how many days did you do moderate physical activities like heavy lifting, digging, aerobics, or fast bicycling?
gdf = (
    aarhus.query(
        "`41 During the last 7 days, on how many days did you do moderate physical activities like heavy lifting, digging, aerobics, or fast bicycling?` < 7"
    )
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "41 During the last 7 days, on how many days did you do moderate physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
            "mean",
        ),
        std=(
            "41 During the last 7 days, on how many days did you do moderate physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
            lambda x: sem(x, nan_policy="omit"),
        ),
        count=(
            "41 During the last 7 days, on how many days did you do moderate physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
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
fig.axes[0].set_ylabel("Days")

# %%
## How much time did you usually spend doing moderate physical acitivities on one of those days?
gdf = (
    aarhus.loc[aarhus.iloc[:, 104].apply(lambda x: not isinstance(x, str)), :]
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "42 How much time did you usually spend doing moderate physical acitivities on one of those days?",
            "mean",
        ),
        std=(
            "42 How much time did you usually spend doing moderate physical acitivities on one of those days?",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "42 How much time did you usually spend doing moderate physical acitivities on one of those days?",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=250)
fig.axes[0].set_ylabel("Minutes")

# %%
## During the last 7 days, on how many days did you walk for at least 10 min at a time?
gdf = (
    aarhus.query(
        "`43 During the last 7 days, on how many days did you walk for at least 10 min at a time?` < 7"
    )
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "43 During the last 7 days, on how many days did you walk for at least 10 min at a time?",
            "mean",
        ),
        std=(
            "43 During the last 7 days, on how many days did you walk for at least 10 min at a time?",
            lambda x: sem(x, nan_policy="omit"),
        ),
        count=(
            "43 During the last 7 days, on how many days did you walk for at least 10 min at a time?",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=20)
fig.axes[0].set_ylabel("Days")

# %%
## How much time did you usually spend walking on one of those days?
gdf = (
    aarhus.loc[aarhus.iloc[:, 106].apply(lambda x: not isinstance(x, str)), :]
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "44 How much time did you usually spend walking on one of those days?",
            "mean",
        ),
        std=(
            "44 How much time did you usually spend walking on one of those days?",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "44 How much time did you usually spend walking on one of those days?",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=250)
fig.axes[0].set_ylabel("Minutes")

# %%
## ALL
## During the last 7 days, how much time did you spend sitting on a week day?
gdf = (
    aarhus.loc[aarhus.iloc[:, 107].apply(lambda x: not isinstance(x, str)), :]
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "45 During the last 7 days, how much time did you spend sitting on a week day?",
            "mean",
        ),
        std=(
            "45 During the last 7 days, how much time did you spend sitting on a week day?",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "45 During the last 7 days, how much time did you spend sitting on a week day?",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=600)
fig.axes[0].set_ylabel("Minutes")

# %%
