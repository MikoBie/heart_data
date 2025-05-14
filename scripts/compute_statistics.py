# %%
from heart import PROC
import pandas as pd
import matplotlib.pyplot as plt

# %%
athens = pd.read_excel(PROC / "Athens.xlsx")
aarhus = pd.read_excel(PROC / "Aarhus.xlsx")
belgrade = pd.read_excel(PROC / "Belgrade.xlsx")


# %%
def plot_barplots(
    key: list,
    before: list,
    after: list,
    title: str,
    before_label: str = "",
    after_label: str = "",
    percentage=False,
):
    x_names = [k for k in key]
    x_a = [n - 0.25 for n, _ in enumerate(key)]
    x_b = [n + 0.25 for n, _ in enumerate(key)]
    y_a = [a for a in after]
    y_b = [b for b in before]
    plt.grid(axis="x", linestyle="--", color="darkgrey")
    ax = plt.gca()
    plt.barh(x_b, y_b, height=0.5, color="#13508d", label=before_label)
    plt.barh(x_a, y_a, height=0.5, color="#70bf58", label=after_label)
    ax.set_yticks(list(range(len(x_names))))
    ax.set_yticklabels(x_names, ha="right")
    if percentage:
        labels = [f"{xtick.get_text()}%" for xtick in ax.get_xticklabels()]
        ax.set_xticklabels(labels)
    plt.title(label=title, loc="center")
    plt.legend()
    plt.show()


# %%
len(aarhus[["city", "user_id"]].groupby("user_id").count().query("city < 2"))
len(belgrade[["city", "user_id"]].groupby("user_id").count().query("city < 2"))
len(athens[["city", "user_id"]].groupby("user_id").count().query("city < 2"))

# %%
print(aarhus[["city", "Sex"]].groupby("Sex").count())
print(belgrade[["city", "Sex"]].groupby("Sex").count())
print(athens[["city", "Sex"]].groupby("Sex").count())

# %%
athens.query("Sex != Sex")[
    ["When do you usually visit the demo site?", "city"]
].groupby("When do you usually visit the demo site?").count()
# %%
df = pd.DataFrame(
    {
        "levels": ["Weekdays", "Weekends", "Both"],
        "before": [3, 18, 18],
        "after": [6, 35, 16],
    }
)
plot_barplots(
    key=df.levels,
    before=df.before,
    after=df.after,
    title="Visits to the demo site (Athens)",
    before_label="before",
    after_label="after",
)

# %%
