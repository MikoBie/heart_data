"""Plot the results from Belgrade: Physical activity"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import (
    plot_comparison_barplots,
    plot_barhplot,
    plot_barplot,
    plot_tests,
)
from heart.utils import prepare_tests
from scipy.stats import sem
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon


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

ids = belgrade.query("version == 'final'")["user_id"].tolist()
belgrade_tests = belgrade.query("user_id in @ids").reset_index(drop=True)

# %%
## FIRST VISIT
## When you are working, which of the following best describes what you do?
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = (
        tdf.groupby("19 Sex")[
            "46 When you are working, which of the following best describes what you do?"
        ]
        .value_counts()
        .reset_index()
    )

    fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=18)
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## When you are working, which of the following best describes what you do?
gdf = (
    belgrade.query("version == 'final'")
    .groupby("19 Sex")[
        "46 When you are working, which of the following best describes what you do?"
    ]
    .value_counts()
    .reset_index()
)

fig = plot_barplot(gdf=gdf, font_size=7, wrap_length=17)
fig.suptitle("Ada Ciganlija --  final visit", fontsize=12, weight="bold")

# %%
## FIRST VISIT
## Do you smoke tabacco?
for _, tdf in belgrade.query("version == 'first'").groupby("park_planned"):
    gdf = tdf["47 Do you smoke tabacco?"].value_counts().reset_index()
    fig = plot_barhplot(
        df=gdf, x="47 Do you smoke tabacco?", y="count", percenteges=True, labels=False
    )
    fig.suptitle(f"{_} -- first visit", fontsize=12, weight="bold")

# %%
## FINAL VISIT
## Do you smoke tabacco?
gdf = (
    belgrade.query("version == 'final'")["47 Do you smoke tabacco?"]
    .value_counts()
    .reset_index()
)

fig = plot_barhplot(
    df=gdf,
    x="47 Do you smoke tabacco?",
    y="count",
    percenteges=True,
    labels=False,
    color="green",
)
fig.suptitle("Adja Ciganlija -- final visit", fontsize=12, weight="bold")

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
fig.axes[0].set_ylabel("Days")

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
fig.axes[0].set_ylabel("Days")
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)
# %%
## Vigorous activities days
test_df = prepare_tests(
    belgrade_tests,
    column="39 During the last 7 days, on how many days did you do vigorous physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
)
test_df = test_df.assign(result=lambda x: x["final"] - x["first"])

# %% Parametric test
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %% Non-parametric test
wilcoxon(test_df["result"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, ylim=7, label="Days", sig=False)

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
## Only Ada Ciganlija
## How much time did you usually spend doing vigorous physical activities on one of those days?
gdf = (
    belgrade.loc[belgrade.iloc[:, 102].apply(lambda x: not isinstance(x, str)), :]
    .query("version == 'final' | park_planned == 'Ada Ciganlija'")
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
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## Vigorous activities minutes
test_df = prepare_tests(
    belgrade_tests,
    column="40 How much time did you usually spend doing vigorous physical acitivities on one of those days?",
)
test_df = test_df.assign(result=lambda x: (x["final"] - x["first"]))

# %% Parametric test
ttest_rel(test_df["final"].tolist(), test_df["first"].tolist(), alternative="greater")

# %% Non-parametric test
wilcoxon(test_df["result"].tolist(), alternative="greater")


# %%
## Plot test
fig = plot_tests(test_df, ylim=250, label="Minutes", sig=False)

# %%
## ALL
## During the last 7 days, on how many days did you do moderate physical activities like heavy lifting, digging, aerobics, or fast bicycling?
gdf = (
    belgrade.groupby(["19 Sex", "version"])
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
## Only Ada Ciganlija
## During the last 7 days, on how many days did you do moderate physical activities like heavy lifting, digging, aerobics, or fast bicycling?
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
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
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## Moderate activities days
test_df = prepare_tests(
    belgrade_tests,
    column="41 During the last 7 days, on how many days did you do moderate physical activities like heavy lifting, digging, aerobics, or fast bicycling?",
)
test_df = test_df.assign(result=lambda x: x["final"] - x["first"])

# %% Parametric test
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %% Non-parametric test
wilcoxon(test_df["result"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, ylim=7, label="Days", sig=False)
# %%
## ALL
## How much time did you usually spend doing moderate physical acitivities on one of those days?
gdf = (
    belgrade.loc[belgrade.iloc[:, 104].apply(lambda x: not isinstance(x, str)), :]
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
## Only Ada Ciganlija
## How much time did you usually spend doing vigorous physical activities on one of those days?
gdf = (
    belgrade.loc[belgrade.iloc[:, 104].apply(lambda x: not isinstance(x, str)), :]
    .query("version == 'final' | park_planned == 'Ada Ciganlija'")
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
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## Moderate activities minutes
test_df = prepare_tests(
    belgrade_tests,
    column="42 How much time did you usually spend doing moderate physical acitivities on one of those days?",
)
test_df = test_df.assign(result=lambda x: (x["final"] - x["first"]))

# %% Parametric test
ttest_rel(test_df["final"].tolist(), test_df["first"].tolist(), alternative="greater")

# %% Non-parametric test
wilcoxon(test_df["result"].tolist(), alternative="greater")


# %%
## Plot test
fig = plot_tests(test_df, ylim=150, label="Minutes", sig=False)


# %%
## ALL
## During the last 7 days, on how many days did you walk for at least 10 min at a time?
gdf = (
    belgrade.query(
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
## Only Ada Ciganlija
## During the last 7 days, on how many days did you walk for at least 10 min at a time?
gdf = (
    belgrade.query(
        "`43 During the last 7 days, on how many days did you walk for at least 10 min at a time?` < 7"
    )
    .query("version == 'final' | park_planned == 'Ada Ciganlija'")
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

fig = plot_comparison_barplots(gdf=gdf, max_value=7.5)
fig.axes[0].set_ylabel("Days")
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## Walking days
test_df = prepare_tests(
    belgrade_tests,
    column="43 During the last 7 days, on how many days did you walk for at least 10 min at a time?",
)
test_df = test_df.assign(result=lambda x: x["final"] - x["first"])

# %% Parametric test
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %% Non-parametric test
wilcoxon(test_df["result"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, ylim=7, label="Days", sig=False)

# %%
## ALL
## How much time did you usually spend walking on one of those days?
gdf = (
    belgrade.loc[belgrade.iloc[:, 106].apply(lambda x: not isinstance(x, str)), :]
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
## Only Ada Ciganlija
## How much time did you usually spend walking on one of those days?
gdf = (
    belgrade.loc[belgrade.iloc[:, 106].apply(lambda x: not isinstance(x, str)), :]
    .query("version == 'final' | park_planned == 'Ada Ciganlija'")
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
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## ALL
## During the last 7 days, how much time did you spend sitting on a week day?
gdf = (
    belgrade.loc[belgrade.iloc[:, 107].apply(lambda x: not isinstance(x, str)), :]
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
## Walking minutes
test_df = prepare_tests(
    belgrade_tests,
    column="44 How much time did you usually spend walking on one of those days?",
)
test_df = test_df.assign(result=lambda x: (x["final"] - x["first"]))

# %% Parametric test
ttest_rel(test_df["final"].tolist(), test_df["first"].tolist(), alternative="greater")

# %% Non-parametric test
wilcoxon(test_df["result"].tolist(), alternative="greater")


# %%
## Plot test
fig = plot_tests(test_df, ylim=250, label="Minutes", sig=False)

# %%
## Only Ada Ciganlija
## How much time did you usually spend sitting on one of those days?
gdf = (
    belgrade.loc[belgrade.iloc[:, 107].apply(lambda x: not isinstance(x, str)), :]
    .query("version == 'final' | park_planned == 'Ada Ciganlija'")
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
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## Sitting minutes
test_df = prepare_tests(
    belgrade_tests,
    column="45 During the last 7 days, how much time did you spend sitting on a week day?",
)
test_df = test_df.assign(result=lambda x: x["first"] - x["final"])

# %% Parametric test
ttest_rel(test_df["first"].tolist(), test_df["final"].tolist(), alternative="greater")

# %% Non-parametric test
wilcoxon(test_df["result"].tolist(), alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, ylim=550, label="Minutes", sig=False)
# %%
