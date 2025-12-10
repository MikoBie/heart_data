"""Plot the results from belgrade: Social"""

# %%
from heart import PROC
import pandas as pd
from heart.plots import plot_tests
from heart.utils import prepare_tests
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon

# %%
## Read data
LIVABILITY = {
    "Friendliness": "friendliness",
    "Attractiveness": "attractiveness",
    "Accessibility": "accessibility",
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
## Place attachment
test_df = prepare_tests(belgrade_tests, column="place_attachment")
test_df = test_df.assign(result=lambda x: x["final"] - x["first"])

# %%
## Parametric test
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %%
## Non-parametric test
wilcoxon(test_df["final"], test_df["first"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, ylim=7, label="Place Attachment", sig=False)

# %%
## Social cohesion
test_df = prepare_tests(belgrade_tests, column="social_cohesion")
test_df = test_df.assign(result=lambda x: x["final"] - x["first"])

# %%
## Parametric test
ttest_rel(test_df["final"], test_df["first"], alternative="greater")

# %%
## Non-parametric test
wilcoxon(test_df["final"], test_df["first"], alternative="greater")

# %%
## Plot test
fig = plot_tests(test_df, ylim=7, label="Social Cohesion", sig=False)
# %%
