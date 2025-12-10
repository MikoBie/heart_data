"""Plot the results from Belgrade: psychological questions"""

# %%
from heart import PROC, PNG
import pandas as pd
from heart.plots import plot_comparison_barplots, plot_tests
from heart.utils import prepare_tests
from scipy.stats import sem
from scipy.stats import ttest_rel


# %%
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
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1,
    color="black",
    weight="bold",
    size="large",
)
fig.savefig(PNG / "swls.png", dpi=200, bbox_inches="tight")

# %%
## Satisfaction With Life Scale Tests
test_df = prepare_tests(belgrade_tests, column="swls")
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, ylim=35, label="Satisfaction With Life Scale")

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
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1,
    color="black",
    weight="bold",
    size="large",
)
fig.savefig(PNG / "wellbeing.png", dpi=200, bbox_inches="tight")

# %%
## Warwick wellbeing test
test_df = prepare_tests(belgrade_tests, column="warwick_wellbeing")
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %%
## Plot test
fig = plot_tests(
    test_df, label="The Warwick-Edinburgh Mental Wellbeing\n Scales", ylim=35, sig=False
)

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
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)
fig.savefig(PNG / "loneliness.png", dpi=200, bbox_inches="tight")

# %%
## UCLA loneliness test
test_df = prepare_tests(belgrade_tests, column="ucla_loneliness")
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, label="UCLA Loneliness Test", ylim=9, sig=False)

# %%
## ALL
## DAAS Depresion scale
gdf = (
    belgrade.groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_depression",
            "mean",
        ),
        std=(
            "dass_depression",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_depression",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=54)
fig.axes[0].set_ylabel("Depression")


# %%
## Only Ada Ciganlija
## DASS Depression Scale
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_depression",
            "mean",
        ),
        std=(
            "dass_depression",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_depression",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=54, fig_size=(3, 3))
fig.axes[0].set_ylabel("Depression")
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)
# %%
## DASS depression test
test_df = prepare_tests(belgrade_tests, column="dass_depression")
ttest_rel(test_df["final"], test_df["first"], alternative="less")

# %%
## Plot test
fig = plot_tests(test_df, label="DASS Depression Scale", ylim=54, sig=False)

# %%
## ALL
## DAAS Anxiety scale
gdf = (
    belgrade.groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_anxiety",
            "mean",
        ),
        std=(
            "dass_anxiety",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_anxiety",
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

fig = plot_comparison_barplots(
    gdf=gdf,
    max_value=54,
)
fig.axes[0].set_ylabel("Depression")

# %%
## Only Ada Ciganlija
## Dass Anxiety Scale
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_anxiety",
            "mean",
        ),
        std=(
            "dass_anxiety",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_anxiety",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=54, fig_size=(3, 3))
fig.axes[0].set_ylabel("Anxiety")
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## DASS anxiety test
test_df = prepare_tests(belgrade_tests, column="dass_anxiety")
ttest_rel(test_df["final"], test_df["first"], alternative="less")

# %%
## Plot test
fig = plot_tests(test_df, label="DASS Anxiety Scale", ylim=54, sig=False)

# %%
## ALL
## DAAS Stress scale
gdf = (
    belgrade.groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_stress",
            "mean",
        ),
        std=(
            "dass_stress",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_stress",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=54, fig_size=(3, 3))
fig.axes[0].set_ylabel("Stress")

# %%
## Only Ada Ciganlija
## DASS Stress scale
gdf = (
    belgrade.query("version == 'final' | park_planned == 'Ada Ciganlija'")
    .groupby(["19 Sex", "version"])
    .agg(
        mean=(
            "dass_stress",
            "mean",
        ),
        std=(
            "dass_stress",
            lambda x: sem(x.astype(float), nan_policy="omit"),
        ),
        count=(
            "dass_stress",
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

fig = plot_comparison_barplots(gdf=gdf, max_value=54, fig_size=(3, 3))
fig.axes[0].set_ylabel("Stress")
fig.suptitle(
    t="Ada Ciganlija",
    horizontalalignment="center",
    y=1.0,
    color="black",
    weight="bold",
    size="large",
)

# %%
## DASS stress test
test_df = prepare_tests(belgrade_tests, column="dass_stress")
ttest_rel(test_df["final"], test_df["first"], alternative="less")

# %%
fig = plot_tests(test_df, label="DASS Stress Scale", ylim=54, sig=False)

# %%
