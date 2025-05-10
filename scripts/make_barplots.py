# %%
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import re

# %%

df_aarhus = pd.DataFrame(
    {
        "age": [
            "0-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",
            "80-89",
            "90+",
        ],
        "before_m": [186, 123, 1344, 617, 275, 258, 247, 183, 99, 22],
        "after_m": [166, 118, 1381, 553, 260, 263, 248, 186, 102, 23],
        "before_f": [185, 138, 1526, 445, 223, 258, 263, 263, 220, 81],
        "after_f": [166, 128, 1470, 438, 203, 251, 265, 264, 231, 70],
    }
)

df_aarhus_mun = pd.DataFrame(
    {
        "age": [
            "0-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",
            "80-89",
            "90+",
        ],
        "before_m": [1852, 1357, 17974, 5429, 2540, 2534, 2167, 1423, 469, 78],
        "after_m": [1690, 1434, 18764, 5552, 2362, 2713, 2159, 1635, 511, 76],
        "before_f": [1874, 1562, 20157, 4511, 2314, 2651, 2320, 1808, 904, 298],
        "after_f": [1642, 1695, 21354, 4472, 2222, 2854, 2403, 1944, 968, 264],
    }
)

df_aarhus_education = pd.DataFrame(
    {
        "level": [
            "Primary education",
            "Upper secondary education",
            "Vocational Education and Training",
            "Short cycle higher education",
            "Vocational bachelors educations",
            "Bachelors programs",
            "Masters programs",
            "PhD programs",
        ],
        "before_m": [24318, 23534, 26220, 7663, 17153, 6028, 19623, 2558],
        "after_m": [24364, 24523, 25114, 7673, 17497, 6395, 20520, 2733],
        "before_f": [21127, 25238, 21053, 5648, 27167, 7056, 21116, 1906],
        "after_f": [20804, 26500, 19967, 5570, 27190, 7507, 22450, 2132],
    }
)

df_aarhus_employment = pd.DataFrame(
    {
        "job": [
            "Agriculture, forestry\nand fishery",
            "Industry, raw material\nextraction and utility company",
            "Construction and landscape",
            "Commerce and transportation",
            "Information and communication",
            "Finance and insurance",
            "Real estate and renting",
            "Business services",
            "Administration, teaching\nand health",
            "Culture, leisure\nand other services",
        ],
        "before": [785, 16088, 10779, 55193, 14732, 5724, 3385, 33335, 75440, 11161],
        "after": [882, 16034, 11327, 59483, 15914, 5894, 4150, 35759, 79011, 11102],
    }
)

df_aarhus_unemployment = pd.DataFrame(
    {
        "dates": [
            "2019.01",
            "2019.02",
            "2019.03",
            "2019.04",
            "2019.05",
            "2019.06",
            "2019.07",
            "2019.08",
            "2019.09",
            "2019.10",
            "2019.11",
            "2019.12",
            "2020.01",
            "2020.02",
            "2020.03",
            "2020.04",
            "2020.05",
            "2020.06",
            "2020.07",
            "2020.08",
            "2020.09",
            "2020.10",
            "2020.11",
            "2020.12",
            "2021.01",
            "2021.02",
            "2021.03",
            "2021.04",
            "2021.05",
            "2021.06",
            "2021.07",
            "2021.08",
            "2021.09",
            "2021.10",
            "2021.11",
            "2021.12",
        ],
        "total": [
            4.5,
            4.6,
            4.4,
            4.1,
            4.1,
            4.4,
            4.9,
            5,
            4.5,
            4.4,
            4.3,
            4.3,
            4.6,
            4.7,
            5,
            5.7,
            5.9,
            6.2,
            6.8,
            6.3,
            5.7,
            5.5,
            5.2,
            5.2,
            5.5,
            5.7,
            5.3,
            4.9,
            4.4,
            4.4,
            5,
            4.5,
            3.7,
            3.5,
            3.2,
            2.8,
        ],
        "men": [
            4.3,
            4.4,
            4.3,
            3.9,
            3.9,
            4.1,
            4.6,
            4.6,
            4.1,
            4.2,
            4.1,
            4.2,
            4.4,
            4.6,
            4.9,
            5.7,
            5.9,
            6,
            6.5,
            6,
            5.5,
            5.3,
            5.2,
            5.2,
            5.5,
            5.7,
            5.3,
            4.9,
            4.4,
            4.3,
            4.9,
            4.3,
            3.6,
            3.4,
            3.1,
            2.8,
        ],
        "women": [
            4.8,
            4.8,
            4.6,
            4.2,
            4.4,
            4.7,
            5.2,
            5.3,
            4.8,
            4.7,
            4.5,
            4.4,
            4.8,
            4.8,
            5,
            5.7,
            5.9,
            6.4,
            7,
            6.6,
            5.9,
            5.6,
            5.2,
            5.2,
            5.5,
            5.6,
            5.3,
            4.9,
            4.5,
            4.5,
            5.2,
            4.6,
            3.9,
            3.6,
            3.2,
            2.7,
        ],
    }
)


df_athens = pd.DataFrame(
    {
        "age": [
            "0-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",
            "80+",
        ],
        "before_m_1": [2322, 2519, 6855, 7180, 5407, 4218, 3499, 2682, 1826],
        "before_m_6": [4847, 5097, 11154, 12549, 9860, 7531, 5402, 4251, 2715],
        "before_m_7": [4420, 4789, 9370, 10215, 8216, 6851, 5193, 4253, 2801],
        "before_f_1": [2305, 2308, 5605, 5995, 5371, 5523, 4570, 4167, 3458],
        "before_f_6": [4723, 4730, 8470, 9899, 10087, 9332, 7244, 7063, 5628],
        "before_f_7": [4056, 4802, 10268, 10436, 9992, 8830, 7303, 6758, 5295],
    }
)

df_belgrade = pd.DataFrame(
    {
        "age": [
            "0-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",
            "80+",
        ],
        "before_f": [
            43402 + 41036,
            37856 + 36395,
            43459 + 57707,
            67986 + 69424,
            65060 + 57943,
            55883 + 59611,
            68507 + 65977,
            39184 + 36108,
            26554 + 18413,
        ],
        "before_m": [
            46042 + 43248,
            39924 + 38354,
            44716 + 53643,
            63422 + 66481,
            61630 + 54279,
            49954 + 50016,
            55490 + 49386,
            28494 + 24481,
            17010 + 10057,
        ],
        "after_m": [
            44294 + 44422,
            42876 + 40637,
            41855 + 49389,
            54639 + 63036,
            65813 + 60715,
            53425 + 48463,
            47009 + 49282,
            41442 + 21469,
            16133 + 10954,
        ],
        "after_f": [
            41152 + 41982,
            40799 + 38946,
            42015 + 51413,
            58531 + 67560,
            69225 + 64941,
            57778 + 54958,
            57364 + 63802,
            59084 + 32572,
            26234 + 20050,
        ],
    }
)

df_kalemegdan = pd.DataFrame(
    {
        "age": [
            "0-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",
            "80+",
        ],
        "before_f": [
            1384 + 897,
            687 + 742,
            1025 + 1601,
            2082 + 2031,
            1843 + 1432,
            1487 + 1668,
            2160 + 2417,
            1371 + 1169,
            872 + 911,
        ],
        "before_m": [
            1378 + 920,
            784 + 765,
            896 + 1353,
            1746 + 1679,
            1537 + 1253,
            1135 + 1178,
            1440 + 1497,
            948 + 774,
            444 + 371,
        ],
        "after_m": [
            980 + 962,
            948 + 858,
            922 + 1170,
            1435 + 1691,
            1765 + 1597,
            1353 + 1189,
            1185 + 1353,
            1342 + 741,
            516 + 376,
        ],
        "after_f": [
            923 + 989,
            931 + 834,
            967 + 1317,
            1606 + 1946,
            1980 + 1883,
            1556 + 1488,
            1578 + 1890,
            2009 + 1087,
            850 + 761,
        ],
    }
)

df_ada = pd.DataFrame(
    {
        "age": [
            "0-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
            "70-79",
            "80+",
        ],
        "before_f": [
            3856 + 4184,
            4027 + 4094,
            4744 + 5987,
            7095 + 7411,
            7036 + 6322,
            6012 + 6493,
            7395 + 6978,
            4206 + 3853,
            2696 + 1563,
        ],
        "before_m": [
            4056 + 4568,
            4260 + 4222,
            4770 + 5672,
            6655 + 6784,
            6581 + 5880,
            5414 + 5248,
            5867 + 5098,
            2968 + 2672,
            1879 + 1040,
        ],
        "after_m": [
            4415 + 4544,
            4561 + 4330,
            4409 + 4974,
            5584 + 6542,
            6750 + 6365,
            5709 + 5140,
            4910 + 5175,
            4360 + 2260,
            1783 + 1184,
        ],
        "after_f": [
            4267 + 4357,
            4263 + 4054,
            4389 + 5215,
            5978 + 6982,
            7350 + 6844,
            6314 + 5857,
            6140 + 6842,
            6258 + 3513,
            2806 + 1996,
        ],
    }
)

df_ada_education = pd.DataFrame(
    {
        "level": [
            "Primary education",
            "Secondary education",
            "Trade/technical/\nvocational training",
            "High-school education",
            "Higher education",
        ],
        "before": [12.3, 54.5, 31.50, 9.04, 19.55],
        "after": [9.5, 52.1, 35.1, 9.1, 27.2],
    }
)

df_kalemegden_education = pd.DataFrame(
    {
        "level": [
            "Primary education",
            "Secondary education",
            "Trade/technical/\nvocational training",
            "High-school education",
            "Higher education",
        ],
        "before": [7.3, 40.8, 21.5, 9.6, 40.5],
        "after": [7.4, 43.5, 19.5, 8.4, 46.7],
    }
)
df_belgrade_employment = pd.DataFrame(
    {
        "job": [
            "Product Processing",
            "Accommodation\n& Catering Services",
            "Wholesale & Retail Trade",
            "Professional Scientific\n& Technical Services",
            "Education",
            "Construction",
            "Administration",
            "Health, Social Services",
        ],
        "before": [119241, 25315, 3136, 52619, 39755, 34292, 56135, 49010],
        "after": [134760, 32383, 4574, 66877, 47124, 46893, 77171, 51788],
    }
)

df_stari_grad_employment = pd.DataFrame(
    {
        "job": [
            "Product Processing",
            "Accommodation\n& Catering Services",
            "Wholesale & Retail Trade",
            "Professional Scientific\n& Technical Services",
            "Education",
            "Construction",
            "Administration",
            "Health, Social Services",
        ],
        "before": [7504, 4053, 436, 7575, 5181, 1731, 6635, 2100],
        "after": [7686, 5014, 611, 10059, 5797, 1485, 6228, 2471],
    }
)

df_cukarica_employment = pd.DataFrame(
    {
        "job": [
            "Product Processing",
            "Accommodation\n& Catering Services",
            "Wholesale & Retail Trade",
            "Professional Scientific\n& Technical Services",
            "Education",
            "Construction",
            "Administration",
            "Health, Social Services",
        ],
        "before": [9387, 1456, 134, 2635, 2744, 2326, 2078, 2366],
        "after": [10134, 2397, 262, 3633, 2985, 3181, 2676, 2770],
    }
)


# %%
def plot_population(
    age: list,
    before_m: list,
    before_f: list,
    after_m: list = [],
    after_f: list = [],
    title: str = "",
):
    rgx = re.compile("\d+")
    x = [n for n, _ in enumerate(age, 1)]
    if len(after_m) and len(after_f):
        y_m = [(after / before) * 100 for before, after in zip(before_m, after_m)]
        y_f = [(-after / before) * 100 for before, after in zip(before_f, after_f)]
    else:
        y_m = [before for before in before_m]
        y_f = [-before for before in before_f]
    ax = plt.gca()
    plt.barh(x, y_m, color="#13508d", label="Before")
    plt.barh(x, y_f, color="#70bf58")
    plt.grid(axis="y", linestyle="--", color="darkgrey")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", which="major", length=0)
    plt.axvline(x=0, color="white")
    plt.yticks(x, age)
    tmp = plt.xticks()
    if len(after_f) and len(after_m):
        plt.axvline(x=-100, color="darkgrey", linewidth=0.5, linestyle="--", ymax=0.95)
        plt.axvline(x=100, color="darkgrey", linewidth=0.5, linestyle="--", ymax=0.95)
        abs_tmp_prec = [f"{int(abs(item))}%" for item in tmp[0]]
        plt.xticks(tmp[0], abs_tmp_prec)
        abs_tmp = [int(abs(item)) for item in tmp[0]]
        plt.text(
            x=sum(abs_tmp) / (len(abs_tmp) + 1),
            y=max(x) + 0.6,
            s="Men",
            horizontalalignment="center",
        )
        plt.text(
            x=-sum(abs_tmp) / (len(abs_tmp) + 1),
            y=max(x) + 0.6,
            s="Women",
            horizontalalignment="center",
        )
    else:
        labels = [
            rgx.search(xtick.get_text()).group() if rgx.search(xtick.get_text()) else ""
            for xtick in ax.get_xticklabels()
        ]
        ax.set_xticklabels(labels)
    plt.title(label=title, loc="center")
    plt.show()


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


def plot_lines(
    dates: list, women: list, men: list, total: list, title: str = "", ylabel: str = ""
):
    x_dates = [datetime.strptime(d, "%Y.%m") for d in dates]
    y_men = [m for m in men]
    y_women = [w for w in women]
    y_total = [t for t in total]
    plt.plot(x_dates, y_men, label="Men", color="#13508d")
    plt.plot(x_dates, y_women, label="Women", color="#70bf58")
    plt.plot(x_dates, y_total, label="Total", color="darkgrey", linestyle="--")
    ax = plt.gca()
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    labels = [f"{ytick.get_text()}%" for ytick in ax.get_yticklabels()]
    ax.set_yticklabels(labels)
    plt.ylabel(ylabel=ylabel)

    plt.title(label=title, loc="center")
    plt.legend()
    plt.show()


# %%
plot_population(
    age=df_aarhus.age,
    before_m=df_aarhus.before_m,
    before_f=df_aarhus.before_f,
    after_m=df_aarhus.after_m,
    after_f=df_aarhus.after_f,
    title="Aarhus (Langenæs Sogn)",
)

# %%
plot_population(
    age=df_athens.age,
    before_m=df_athens.before_m_1,
    before_f=df_athens.before_f_1,
    title="Athens (Mun. 1)",
)
# %%
plot_population(
    age=df_athens.age,
    before_m=df_athens.before_m_6,
    before_f=df_athens.before_f_6,
    title="Athens (Mun. 6)",
)

# %%
plot_population(
    age=df_athens.age,
    before_m=df_athens.before_m_7,
    before_f=df_athens.before_f_7,
    title="Athens (Mun. 7)",
)
# %%
plot_population(
    age=df_aarhus_mun.age,
    before_m=df_aarhus_mun.before_m,
    before_f=df_aarhus_mun.before_f,
    after_m=df_aarhus_mun.after_m,
    after_f=df_aarhus_mun.after_f,
    title="Aarhus (Central Municipality)",
)

# %%
plot_population(
    age=df_aarhus_education.level,
    before_m=df_aarhus_education.before_m,
    before_f=df_aarhus_education.before_f,
    after_m=df_aarhus_education.after_m,
    after_f=df_aarhus_education.after_f,
    title="Aarhus (Central Municipality)",
)

# %%
plot_barplots(
    key=df_aarhus_employment.job,
    before=df_aarhus_employment.before,
    after=df_aarhus_employment.after,
    title="Aarhus",
    before_label=2019,
    after_label=2021,
)

# %%
plot_lines(
    dates=df_aarhus_unemployment.dates,
    men=df_aarhus_unemployment.men,
    women=df_aarhus_unemployment.women,
    total=df_aarhus_unemployment.total,
    title="Aarhus",
    ylabel="Unemployment rate (%)",
)
# %%
plot_population(
    age=df_belgrade.age,
    before_m=df_belgrade.before_m,
    before_f=df_belgrade.before_f,
    after_m=df_belgrade.after_m,
    after_f=df_belgrade.after_f,
    title="Belgrade",
)

# %%
plot_population(
    age=df_ada.age,
    before_m=df_ada.before_m,
    before_f=df_ada.before_f,
    after_m=df_ada.after_m,
    after_f=df_ada.after_f,
    title="ADA Lake",
)
# %%
plot_population(
    age=df_kalemegdan.age,
    before_m=df_kalemegdan.before_m,
    before_f=df_kalemegdan.before_f,
    after_m=df_kalemegdan.after_m,
    after_f=df_kalemegdan.after_f,
    title="Kalemegdan complex",
)
# %%
plot_barplots(
    key=df_ada_education.level,
    before=df_ada_education.before,
    after=df_ada_education.after,
    title="ADA Lake",
    before_label=2011,
    after_label=2022,
    percentage=True,
)

# %%
plot_barplots(
    key=df_kalemegden_education.level,
    before=df_kalemegden_education.before,
    after=df_kalemegden_education.after,
    title="Kalemgdan complex",
    before_label=2011,
    after_label=2022,
    percentage=True,
)


# %%
plot_barplots(
    key=df_belgrade_employment.job,
    before=df_belgrade_employment.before,
    after=df_belgrade_employment.after,
    title="Belgrade",
    before_label=2011,
    after_label=2022,
)

# %%
plot_barplots(
    key=df_stari_grad_employment.job,
    before=df_stari_grad_employment.before,
    after=df_stari_grad_employment.after,
    title="Stari Grad",
    before_label=2011,
    after_label=2022,
)

# %%
plot_barplots(
    key=df_cukarica_employment.job,
    before=df_cukarica_employment.before,
    after=df_cukarica_employment.after,
    title="Cukarica",
    before_label=2011,
    after_label=2022,
)
# %%
