"""Plot the results from Aarhus: psychological questions"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import plot_comparison_barplots, plot_tests
from heart.utils import prepare_tests
from scipy.stats import sem
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon


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
ids = aarhus.query("version == 'final'")["user_id"].tolist()
aarhus_tests = aarhus.query("user_id in @ids").reset_index(drop=True)

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
## Satisfaction With Life Scale
gdf = (
    aarhus.groupby(["19 Sex", "version"])
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
## Satisfaction With Life Scale Tests
test_df = prepare_tests(aarhus_tests, column="swls")
test_df = test_df.assign(result=lambda x: x["final"] - x["first"])

# %%
## Parametric test
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %%
## Non-parametric test
wilcoxon(test_df["final"], test_df["first"], alternative="greater")

# %%
## Plot test
fig = plot_tests(
    test_df,
    ylim=35,
    label="Satisfaction With Life Scale",
    sig=True,
    sig_level="**",
    sig_line=32,
)

# %%
## Warwick wellbeing
gdf = (
    aarhus.groupby(["19 Sex", "version"])
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
## Warwick wellbeing test
test_df = prepare_tests(aarhus_tests, column="warwick_wellbeing")
test_df = test_df.assign(result=lambda x: x["final"] - x["first"])

# %%
## Parametric test
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %%
## Non-parametric test
wilcoxon(test_df["result"], alternative="greater")

# %%
## Plot test
fig = plot_tests(
    test_df, label="The Warwick-Edinburgh Mental Wellbeing\n Scale", ylim=35, sig=False
)

# %%
## UCLA loneliness
gdf = (
    aarhus.groupby(["19 Sex", "version"])
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
## UCLA loneliness test
test_df = prepare_tests(aarhus_tests, column="ucla_loneliness")
test_df = test_df.assign(result=lambda x: x["first"] - x["final"])

# %%
## Parametric test
ttest_rel(test_df["first"], test_df["final"], alternative="greater")

# %%
## Non-parametric test
wilcoxon(test_df["result"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, label="UCLA Loneliness Test", ylim=9, sig=False)

# %%
## DAAS Depresion scale
gdf = (
    aarhus.groupby(["19 Sex", "version"])
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

# %%
## DASS depression test
test_df = prepare_tests(aarhus_tests, column="dass_depression")
test_df = test_df.assign(result=lambda x: x["first"] - x["final"])

# %%
## Parametric test
ttest_rel(test_df["first"], test_df["final"], alternative="greater")

# %%
## Non-parametric test
wilcoxon(test_df["result"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, label="DASS Depression Scale", ylim=54, sig=False)

# %%
## DASS Anxiety scale
gdf = (
    aarhus.groupby(["19 Sex", "version"])
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

# %%
## DASS anxiety test
test_df = prepare_tests(aarhus_tests, column="dass_anxiety")
test_df = test_df.assign(result=lambda x: x["first"] - x["final"])

# %%
## Parametric test
ttest_rel(test_df["first"], test_df["final"], alternative="greater")

# %%
## Non-parametric test
wilcoxon(test_df["result"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, label="DASS Anxiety Scale", ylim=54, sig=False)

# %%
## DAAS Stress scale
gdf = (
    aarhus.groupby(["19 Sex", "version"])
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
## DASS stress test
test_df = prepare_tests(aarhus_tests, column="dass_stress")
test_df = test_df.assign(result=lambda x: x["first"] - x["final"])

# %%
## Parametric test
ttest_rel(test_df["first"], test_df["final"], alternative="greater")

# %%
## Non-parametric test
wilcoxon(test_df["result"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, label="DASS Stress Scale", ylim=54, sig=False)

# %%
