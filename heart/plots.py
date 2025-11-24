import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
from textwrap import wrap
from heart.config import COLORS
from heart.utils import round_label, process_lst
import numpy as np


def plot_barplot(
    gdf: pd.DataFrame,
    wrap_length: int = 10,
    font_size: int = 10,
    COLORS: dict = COLORS,
    perc_size: int = 10,
) -> plt.Figure:
    """Plot a barplot for three category gender.

    Parameters
    ----------
    gdf
        data from polish questionnaire
    wrap_length, optional
        lenght of a string in ax major ticks, by default 10
    font_size, optional
        size of the font of a string in ax major ticks, by default 10
    COLORS, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS

    Returns
    -------
        a matplotlib figure object
    """
    gdf = gdf.assign(codes=lambda x: pd.Categorical(x.iloc[:, 1]).codes)
    major_ticks = dict(zip(gdf.codes, gdf.iloc[:, 1]))
    if len(gdf.loc[:, "19 Sex"].unique().tolist()) > 2:
        location = {"Female": -0.25, "Male": 0, "Prefer not to say": 0.25}
        bar_width = 0.2
    else:
        location = {"Female": -0.25, "Male": 0.25}
        bar_width = 0.45

    fig, axs = plt.subplots(figsize=(4, 4), nrows=1, ncols=1)
    if isinstance(axs, plt.Axes):
        axs = [axs]
    for _, dfg in gdf.groupby("19 Sex"):
        dfg = dfg.reset_index(drop=True).assign(
            perc=lambda x: x.loc[:, "count"] / x.loc[:, "count"].sum() * 100,
            loc=lambda x: x["codes"] + location[_],
        )
        rect = axs[0].bar(
            dfg.loc[:, "loc"].tolist(),
            dfg.loc[:, "perc"].tolist(),
            width=bar_width,
            label=f"{_.capitalize()} (n = {dfg.loc[:, 'count'].sum()})",
            color=COLORS[_],
        )
        axs[0].bar_label(rect, fmt=lambda x: round_label(x), fontsize=perc_size)
    axs[0].set_xticks(list(major_ticks))
    axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
    axs[0].xaxis.set_major_formatter(
        ticker.FuncFormatter(
            lambda x, pos: "\n".join(wrap(str(major_ticks.get(x, "")), wrap_length))
        )
    )
    for spin in axs[0].spines:
        if spin != "bottom" and spin != "left":
            axs[0].spines[spin].set_visible(False)
    axs[0].set_xticks(list(major_ticks))
    axs[0].set_ylim(0, 100)
    axs[0].tick_params(axis="x", which="major", labelsize=font_size)
    fig.legend(
        ncol=2, loc="center", bbox_to_anchor=(0.5, -0.07), fancybox=True, shadow=True
    )
    return fig


def plot_radar(
    dt_ord: dict,
    theta: np.array,
    distance: dict,
    colors: dict = COLORS,
    plot_between: bool = True,
    std: bool = False,
) -> plt.Figure:
    """Plots radar plots.

    Parameters
    ----------
    dt_ord
        a dictionary where keys are groups and vlaues lists of frequencies
    colors, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS
    theta
        the result of radar_factory; it an array with coordinates in polar
    plot_between, optional
        whether to plot the range between min and max values, by default set to True
    std
        whether to plot std based range instead of min, max based range, by default set to False
    distance, optional
        a dictionary with keys as dimensions and values as distances between label and the plot, by default {}

    Returns
    -------
        radar plots
    """
    fig, axs = plt.subplots(
        figsize=(3 * len(dt_ord), 4),
        nrows=1,
        ncols=len(dt_ord),
        subplot_kw=dict(projection="radar"),
    )
    fig.subplots_adjust(wspace=0.5, hspace=0.20, top=0.85, bottom=0.05)
    if len(dt_ord) == 1:
        axs_flat = [axs]
    else:
        axs_flat = axs.flat

    for ax, time in zip(axs_flat, dt_ord):
        ax.set_rgrids([1, 2, 3, 4, 5, 6, 7], visible=False)
        ax.set_ylim(0, 7)
        ax.set_title(
            x=0.5,
            y=-0.3,
            label=time,
            weight="bold",
            size="medium",
            horizontalalignment="center",
            verticalalignment="center",
        )
        if len(dt_ord[time].keys()) < 2:
            ax.plot(
                theta,
                [np.mean(item) for item in dt_ord[time]["first"].values()],
                color=colors["blue"],
            )
            if plot_between:
                ax.fill_between(
                    theta,
                    process_lst(dt_ord[time]["first"].values(), min),
                    process_lst(dt_ord[time]["first"].values(), max),
                    facecolor=colors["blue"],
                    alpha=0.25,
                )
            if not plot_between and std:
                ax.fill_between(
                    theta,
                    process_lst(
                        dt_ord[time]["first"].values(),
                        lambda x: np.mean(x) - np.std(x),
                    ),
                    process_lst(
                        dt_ord[time]["first"].values(),
                        lambda x: np.mean(x) + np.std(x),
                    ),
                    facecolor=colors["blue"],
                    alpha=0.25,
                )

            for t, d in zip(
                theta, process_lst(dt_ord[time]["first"].values(), np.mean)
            ):
                ax.text(
                    t, d + 0.3, f"{d:.1f}", horizontalalignment="center", fontsize=6
                )
            ax.set_varlabels(
                dt_ord[time]["first"].keys(),
                kwargs={
                    "fontsize": 6,
                    "verticalalignment": "center",
                    "horizontalalignment": "center",
                },
            )
        else:
            ax.plot(
                theta,
                [np.mean(item) for item in dt_ord[time]["first"].values()],
                color=colors["blue"],
            )
            ax.plot(
                theta,
                [np.mean(item) for item in dt_ord[time]["final"].values()],
                color=colors["green"],
            )

            labels = []
            for d, first, final in zip(
                distance,
                process_lst(dt_ord[time]["first"].values(), np.mean),
                process_lst(dt_ord[time]["final"].values(), np.mean),
            ):
                labels.append(f"{d}\n({((final - first) / first) * 100:.1f}%)")
            ax.set_varlabels(
                labels,
                kwargs={
                    "fontsize": 6,
                    "verticalalignment": "center",
                    "horizontalalignment": "center",
                },
            )
        for label in ax.get_xticklabels():
            label.set_position(
                distance.get(label.get_text().split("\n(")[0], [0, -0.1])
            )
    return fig


def plot_comparison_barplots(
    gdf: pd.DataFrame,
    max_value: int,
    font_size: int = 10,
    COLORS: dict = COLORS,
    fig_size: tuple = (4, 4),
) -> plt.Figure:
    """
    Plot comparison barplots for means by sex and questionnaire version.

    Parameters
    ----------
    gdf : pd.DataFrame
        DataFrame containing columns for questionnaire version, sex, mean, and standard deviation.
        Expected columns: 'version', '19 Sex', 'mean', 'std'.
    max_value: int
        Maximum value on yaxis.
    wrap_length : int, optional
        Length of string in axis major ticks, by default 10.
    font_size : int, optional
        Font size for axis major ticks, by default 10.
    COLORS : dict, optional
        Dictionary mapping sex categories to color hex codes, by default COLORS.

    Returns
    -------
    matplotlib.figure.Figure
        A matplotlib figure object with the comparison barplots.
    """
    gdf = gdf.assign(codes=lambda x: pd.Categorical(x.iloc[:, 1]).codes)
    major_ticks = dict(zip(gdf.codes, gdf.iloc[:, 1]))
    if len(gdf.loc[:, "19 Sex"].unique().tolist()) > 2:
        location = {"Female": -0.25, "Male": 0, "Prefer not to say": 0.25}
        bar_width = 0.2
    else:
        location = {"Female": -0.25, "Male": 0.25}
        bar_width = 0.45

    fig, axs = plt.subplots(figsize=fig_size, nrows=1, ncols=1)
    if isinstance(axs, plt.Axes):
        axs = [axs]
    for _, dfg in gdf.groupby("version", observed=True):
        dfg = dfg.reset_index(drop=True).assign(
            loc=lambda x: x.apply(lambda x: x["codes"] + location[x["19 Sex"]], axis=1),
        )
        rect = axs[0].bar(
            dfg.loc[:, "loc"].tolist(),
            dfg.loc[:, "mean"].tolist(),
            yerr=dfg.loc[:, "std"].tolist(),
            width=bar_width,
            capsize=2,
            color=[COLORS[item] for item in dfg["19 Sex"].tolist()],
            label=dfg["19 Sex"].tolist(),
        )
        axs[0].bar_label(rect, fmt=lambda x: round(x, 2), fontsize=9)
    axs[0].set_xticks(list(major_ticks))
    for spin in axs[0].spines:
        if spin != "bottom" and spin != "left":
            axs[0].spines[spin].set_visible(False)
    axs[0].set_xticks(list(major_ticks))
    axs[0].xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: {0: "Before", 1: "After"}.get(x, ""))
    )
    axs[0].set_ylim(0, max_value)
    axs[0].tick_params(axis="x", which="major", labelsize=font_size)
    axs[0].ticklabel_format(axis="y", style="plain")
    handles, labels = axs[0].get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    fig.legend(
        by_label.values(),
        by_label.keys(),
        ncol=3,
        loc="center",
        bbox_to_anchor=(0.5, -0.03),
        fancybox=True,
        shadow=True,
    )
    return fig


def plot_barhplot(
    df: pd.DataFrame,
    y: str,
    x: str,
    padding: int = 1,
    labels: bool = True,
    percenteges: bool = False,
    color: str = "blue",
    COLORS: dict = COLORS,
) -> plt.Figure:
    """Plot horizontal barplots

    Parameters
    ----------
    df
        data frame with frequencies.
    y
        column with frequencies
    x
        column with categories
    padding, optional
        the distance to the frequency to barplot, by default 10
    labels
        whether to display bar labels, by default True. percentegaes must be set to False
    percenteges
        whether to show percenteges, by default False. labels must be set to False
    color
        color to the barplot, by default "blue". The colors must be among the keys of the COLORS dictionary
    COLORS
        a dictionary with keys names and values hashes of the colors, by default
        COLORS


    Returns
    -------
       plt.Figure
    """
    fig = plt.figure(figsize=(6, 4))
    if labels and not percenteges:
        rects = plt.barh(df[x].tolist(), df[y].tolist(), color=COLORS[color])
        fig.axes[0].bar_label(rects, padding=padding, fmt=lambda x: int(round(x, 0)))
    if not labels and percenteges:
        df = df.assign(perc=lambda x: 100 * x["count"] / x["count"].sum())
        rects = plt.barh(df[x].tolist(), df["perc"].tolist(), color=COLORS[color])
        fig.axes[0].bar_label(
            rects, padding=padding, fmt=lambda x: f"{int(round(x, 0))}%"
        )
        fig.axes[0].set_xlim(0, 100)
        fig.axes[0].xaxis.set_major_formatter(ticker.PercentFormatter())

    return fig


def plot_sex_barhplot(
    df: pd.DataFrame,
    COLORS: dict = COLORS,
    labels_size: int = 10,
    male_n: int = 6,
    female_n: int = 10,
    other_n: int = 3,
) -> plt.Figure:
    """Plots a horizontal bar plot for the data prepared by `prepare_data`.

    Parameters
    ----------
    df
        a data frame containing the data

    COLORS, optional
        a dictionary with keys blue and green and values hexes of colors, by default COLORS

    Returns
    -------
        a matplotlib figure object.
    """
    if "Prefer not to say" in df.columns:
        fig, axs = plt.subplots(figsize=(9, 4), nrows=1, ncols=3)
        rect = axs[2].barh(
            df["names"],
            df["Prefer not to say"],
            color=COLORS["Prefer not to say"],
            label=f"Prefer not to say (n = {other_n})",
        )
        axs[2].bar_label(rect, padding=1, fmt=lambda x: round_label(x))
        axs[2].set_yticks([])
    else:
        fig, axs = plt.subplots(figsize=(6, 4), nrows=1, ncols=2)

    rect = axs[0].barh(
        df["names"], df["Male"], color=COLORS["blue"], label=f"Male (n = {male_n})"
    )
    axs[0].bar_label(rect, padding=1, fmt=lambda x: round_label(x))
    axs[0].tick_params(axis="y", which="major", labelsize=labels_size)
    rect = axs[1].barh(
        df["names"],
        df["Female"],
        color=COLORS["green"],
        label=f"Female (n = {female_n})",
    )
    axs[1].bar_label(rect, padding=1, fmt=lambda x: round_label(x))
    axs[1].set_yticks([])
    for ax in axs:
        for spin in ax.spines:
            if spin != "bottom" and spin != "left":
                ax.spines[spin].set_visible(False)
        ax.xaxis.set_major_formatter(ticker.PercentFormatter())
        ax.set_xlim(0, 100)
    return fig
