import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
from textwrap import wrap
from heart.config import COLORS
from heart.utils import round_label


def plot_barplot(
    gdf: pd.DataFrame, COLORS: dict = COLORS, font_size: int = 10, wrap_length: int = 10
) -> plt.Figure:
    """Plots a bar plot for the wearables data.

    Parameters
    ----------
    df
        data from the wearables questionnaire.

    COLORS, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS

    font_size, optional
        the size of the xaxis major tick labels, by default 10

    wrap_length, optional
        the length of the string in line of the xaxis major tick labels, by default 10

    Returns
    -------
        a matplotlib figure object with one subplot.
    """
    gdf = gdf.assign(codes=lambda x: pd.Categorical(x.iloc[:, 1]).codes)
    major_ticks = dict(zip(gdf.codes, gdf.iloc[:, 1]))
    fig, axs = plt.subplots(figsize=(4, 4), nrows=1, ncols=1)
    if isinstance(axs, plt.Axes):
        axs = [axs]

    for (
        n,
        ax,
    ) in enumerate(axs):
        female = (
            gdf[gdf.iloc[:, 0] == "Female"]
            .reset_index(drop=True)
            .assign(
                perc=lambda x: x.iloc[:, 2] / x.iloc[:, 2].sum() * 100,
                loc=lambda x: x["codes"] - 0.25,
            )
        )
        male = (
            gdf[gdf.iloc[:, 0] == "Male"]
            .reset_index(drop=True)
            .assign(
                perc=lambda x: x.iloc[:, 2] / x.iloc[:, 2].sum() * 100,
                loc=lambda x: x["codes"] + 0.25,
            )
        )
        female_rect = ax.bar(
            female.loc[:, "loc"].tolist(),
            female.loc[:, "perc"].tolist(),
            width=0.45,
            label=f"Female (n = {female['count'].sum()})",
            color=COLORS["green"],
        )
        male_rect = ax.bar(
            male.loc[:, "loc"].tolist(),
            male.loc[:, "perc"].tolist(),
            width=0.45,
            label=f"Male (n = {male['count'].sum()})",
            color=COLORS["blue"],
        )
        ax.bar_label(female_rect, fmt=lambda x: round_label(x))
        ax.bar_label(male_rect, fmt=lambda x: round_label(x))
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter())
        ax.xaxis.set_major_formatter(
            ticker.FuncFormatter(
                lambda x, pos: "\n".join(wrap(str(major_ticks.get(x, "")), wrap_length))
            )
        )
        ax.set_xticks(list(major_ticks))
        ax.tick_params(axis="x", which="major", labelsize=font_size)

        for spin in ax.spines:
            if spin != "bottom" and spin != "left":
                ax.spines[spin].set_visible(False)
            elif spin == "left" and n != 0:
                ax.spines[spin].set_visible(False)
        if n != 0:
            ax.set_yticks([])
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        ncol=2,
        loc="center",
        bbox_to_anchor=(0.5, -0.03),
        fancybox=True,
        shadow=True,
    )
    return fig
