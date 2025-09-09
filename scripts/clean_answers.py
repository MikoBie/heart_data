"""Script to clean and translate answers for local languages."""

# %%
import pandas as pd
from heart import PROC
from heart.mappings import aarhus_a_dct, belgrade_a_dct, athens_a_dct
from typing import Any
import numpy as np

# %%
athens = pd.read_excel(PROC / "Athens.xlsx")
belgrade = pd.read_excel(PROC / "Belgrade.xlsx")
aarhus = pd.read_excel(PROC / "Aarhus.xlsx")

dct_df = {
    "Athens": {"df": athens, "mapping": athens_a_dct},
    "Belgrade": {"df": belgrade, "mapping": belgrade_a_dct},
    "Aarhus": {"df": aarhus, "mapping": aarhus_a_dct},
}


# %%
def translate_answers(df: pd.DataFrame, mappings: dict) -> pd.DataFrame:
    """
    Translates answers int the data frame from local languages to English.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the answers to be translated.
    mappings : dict
        Dictionary containing the mappings for translation.

    Returns:
    --------
    pd.DataFrame
        DataFrame with translated answers.
    """
    return df.map(lambda x: mappings.get(x, x) if isinstance(x, str) else x)


def split_string(s: str) -> list:
    """
    Splits a string by commas and strips whitespace.

    Parameters:
    -----------
    s : str
        Input string to be split.

    Returns:
    --------
    list
        List of cleaned strings.
    """
    if not isinstance(s, str):
        return []
    return [item.strip() for item in s.split(",")]


def clean_answer(el: Any, mapping: dict) -> str | Any:
    """
    Returns a cleaned string by stripping whitespace and converting numbers to strings. It maps the string to meanigful answers. If the input is not a string or number, it returns the input as is.

    Parameters:
    -----------
    el : Any
        Input element to be cleaned.
    mapping : dict
        Dictionary containing the mappings for translation.

    Returns:
    --------
    str|Any
        cleaned string or element as it was (if the intput was different thana a string or number).
    """
    if isinstance(el, float) and pd.notna(el):
        el = str(int(el)).strip()
    elif isinstance(el, int):
        el = str(el).strip()
    elif isinstance(el, str):
        el = el.strip()
    return mapping.get(el, el)


def copy_demographics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Copies demographics data for users with multiple entries.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the survey data.

    Returns:
    --------
    pd.DataFrame
        DataFrame with demographics data copied for users with multiple
        entries."""
    output = pd.DataFrame()

    for item in df.loc[:, "user_id"].unique():
        tmp = df.query(f"user_id == {item}")
        if tmp.shape[0] > 1:
            ## TODO: check a better way to do this. So far it just supresses a warning.
            with pd.option_context("future.no_silent_downcasting", True):
                tmp.loc[
                    :,
                    "18 Age":"31 Do you have access in your neighbourghood to the following services?",
                ] = (
                    tmp.loc[
                        :,
                        "18 Age":"31 Do you have access in your neighbourghood to the following services?",
                    ]
                    .ffill()
                    .bfill()
                )

        output = pd.concat([output, tmp])
    return output


# %%
def main():
    """
    Main function to clean and translate answers in the datasets.
    """
    global dct_df
    for key, value in dct_df.items():
        df = value["df"]
        mapping = value["mapping"]
        df = df.astype("object")
        df.loc[:, df.filter(like="1 Have").columns] = df.loc[
            :, df.filter(like="1 Have").columns
        ].map(lambda x: clean_answer(x, {"1": "Yes", "2": "No"}))

        df.loc[:, df.filter(like="2 How do").columns] = df.loc[
            :, df.filter(like="2 How do").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Walk",
                    "2": "Public transport",
                    "3": "Bicycle, ,scooter, etc.",
                    "4": "Car",
                    "5": "Combination of the above",
                },
            )
        )

        df.loc[:, df.filter(like="3 How long").columns] = df.loc[
            :, df.filter(like="3 How long").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "1-10 minutes",
                    "2": "11-15 minutes",
                    "3": "16-30 minutes",
                    "4": "31-60 minutes",
                    "5": "61-120 minutes",
                    "6": "Longer than 2 hours",
                },
            )
        )

        df.loc[:, df.filter(like="4 When do you").columns] = df.loc[
            :, df.filter(like="4 When do you").columns
        ].map(lambda x: clean_answer(x, {"1": "Weekdays", "2": "Weekend", "3": "Both"}))

        if key == "Belgrade":
            df.loc[:, df.filter(like="5.1 How often").columns] = df.loc[
                :, df.filter(like="5.1 How often").columns
            ].map(
                lambda x: clean_answer(
                    x,
                    {
                        "1": "Everyday",
                        "2": "A few times a week",
                        "3": "Once a week",
                        "4": "Once a month",
                        "5": "Other",
                    },
                )
            )

            df.loc[:, df.filter(like="5.2 How often").columns] = df.loc[
                :, df.filter(like="5.2 How often").columns
            ].map(
                lambda x: clean_answer(
                    x,
                    {
                        "1": "Everyday",
                        "2": "A few times a week",
                        "3": "Once a week",
                        "4": "Once a month",
                        "5": "Other",
                    },
                )
            )

            df.loc[:, df.filter(like="5.3 How often").columns] = df.loc[
                :, df.filter(like="5.3 How often").columns
            ].map(
                lambda x: clean_answer(
                    x,
                    {
                        "1": "Everyday",
                        "2": "A few times a week",
                        "3": "Once a week",
                        "4": "Once a month",
                        "5": "Other",
                    },
                )
            )

            df.loc[:, df.filter(like="5.4 How often").columns] = df.loc[
                :, df.filter(like="5.4 How often").columns
            ].map(
                lambda x: clean_answer(
                    x,
                    {
                        "1": "Everyday",
                        "2": "A few times a week",
                        "3": "Once a week",
                        "4": "Once a month",
                        "5": "Other",
                    },
                )
            )

        df.loc[:, df.filter(like="5.1 How often").columns] = df.loc[
            :, df.filter(like="5.1 How often").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Everyday",
                    "2": "A few times a week",
                    "3": "Once a week",
                    "4": "Once a month",
                    "5": "I don't visit",
                    "6": "Other",
                },
            )
        )

        df.loc[:, df.filter(like="5.2 How often").columns] = df.loc[
            :, df.filter(like="5.2 How often").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Everyday",
                    "2": "A few times a week",
                    "3": "Once a week",
                    "4": "Once a month",
                    "5": "I don't visit",
                    "6": "Other",
                },
            )
        )

        df.loc[:, df.filter(like="5.3 How often").columns] = df.loc[
            :, df.filter(like="5.3 How often").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Everyday",
                    "2": "A few times a week",
                    "3": "Once a week",
                    "4": "Once a month",
                    "5": "I don't visit",
                    "6": "Other",
                },
            )
        )

        df.loc[:, df.filter(like="5.4 How often").columns] = df.loc[
            :, df.filter(like="5.4 How often").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Everyday",
                    "2": "A few times a week",
                    "3": "Once a week",
                    "4": "Once a month",
                    "5": "I don't visit",
                    "6": "Other",
                },
            )
        )

        df.loc[:, df.filter(like="6.1 What time").columns] = df.loc[
            :, df.filter(like="6.1 What time").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Morning (6-10)",
                    "2": "Midday (10-14)",
                    "3": "Afternoon (14-18)",
                    "4": "Evening (18-22)",
                    "5": "Night (22-6)",
                    "6": "I don't visit",
                },
            )
        )

        df.loc[:, df.filter(like="6.2 What time").columns] = df.loc[
            :, df.filter(like="6.2 What time").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Morning (6-10)",
                    "2": "Midday (10-14)",
                    "3": "Afternoon (14-18)",
                    "4": "Evening (18-22)",
                    "5": "Night (22-6)",
                    "6": "I don't visit",
                },
            )
        )

        df.loc[:, df.filter(like="6.3 What time").columns] = df.loc[
            :, df.filter(like="6.3 What time").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Morning (6-10)",
                    "2": "Midday (10-14)",
                    "3": "Afternoon (14-18)",
                    "4": "Evening (18-22)",
                    "5": "Night (22-6)",
                    "6": "I don't visit",
                },
            )
        )

        df.loc[:, df.filter(like="6.4 What time").columns] = df.loc[
            :, df.filter(like="6.4 What time").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Morning (6-10)",
                    "2": "Midday (10-14)",
                    "3": "Afternoon (14-18)",
                    "4": "Evening (18-22)",
                    "5": "Night (22-6)",
                    "6": "I don't visit",
                },
            )
        )

        df.loc[:, df.filter(like="7 What do").columns] = df.loc[
            :, df.filter(like="7 What do").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "predominantly walk",
                    "2": "predominantly sit",
                    "3": "mostly cycle",
                    "4": "mostly use open gym",
                    "5": "Other",
                },
            )
        )

        df["19 Sex"] = df["19 Sex"].map(
            lambda x: clean_answer(
                x, {"1": "Female", "2": "Male", "3": "Prefer not to say"}
            )
        )

        df["20 Gender"] = df["20 Gender"].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Woman",
                    "2": "Man",
                    "3": "Trans Man",
                    "4": "Trans Woman",
                    "5": "Genderqueer/Gender Non-conforming",
                    "6": "I don't know",
                    "7": "Prefer to self-describe",
                    "8": "Prefer not to say",
                },
            )
        )

        df["21 Martial status"] = df["21 Martial status"].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Single",
                    "2": "Married (including a marriage/common-law union)",
                    "3": "Divorced",
                    "4": "Widow/er",
                },
            )
        )

        df["22 Education level"] = df["22 Education level"].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Elementary school",
                    "2": "High school",
                    "3": "Trade/technical/vocational training",
                    "4": "Bachelor's degree",
                    "5": "Master's degree",
                    "6": "PhD",
                    "7": "Prefer not to say",
                },
            )
        )

        df["23 Occupation"] = df["23 Occupation"].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Working full time",
                    "2": "Workin part time",
                    "3": "Unemployed",
                    "4": "Retired and not active",
                    "5": "Retired but active",
                    "6": "Homemaker/umpaid career",
                    "7": "Student",
                    "8": "Unable to work",
                    "9": "Prefer not to say",
                },
            )
        )

        df.loc[:, df.filter(like="29 Are you").columns] = df.loc[
            :, df.filter(like="29 Are you").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Ethnic minority",
                    "2": "Religious minority",
                    "3": "Immigrant group",
                    "4": "Refugees group",
                    "5": "Person with disability",
                    "6": "Person from LGBTQ+ community",
                    "7": "Other",
                    "8": "None of the above",
                },
            )
        )

        df.loc[:, df.filter(like="30 Which").columns] = df.loc[
            :, df.filter(like="30 Which").columns
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Christian catholic",
                    "2": "Christian orthodox",
                    "3": "Christian protestant, protestant",
                    "4": "Other christian denomination",
                    "5": "Jewish",
                    "6": "Muslim",
                    "7": "Hindu",
                    "8": "None/Atheist",
                    "9": "Other",
                    "10": "Prefer not to say",
                },
            )
        )

        df.loc[:, df.filter(like="31 Do").columns] = df.loc[
            :, df.filter(like="31 Do").columns
        ].map(
            lambda x: "; ".join([mapping.get(item, item) for item in split_string(x)])
        )

        df.loc[
            :,
            df.filter(
                like="Please choose the park you have visited in the last three months"
            ).columns,
        ] = df.loc[
            :,
            df.filter(
                like="Please choose the park you have visited in the last three months"
            ).columns,
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Ada Ciganlija",
                    "2": "Košutnjak",
                    "3": "Kalemegdan",
                },
            )
        )

        df.loc[
            :,
            df.filter(
                like="Please choose the park you are going to visit in the next three months"
            ).columns,
        ] = df.loc[
            :,
            df.filter(
                like="Please choose the park you are going to visit in the next three months"
            ).columns,
        ].map(
            lambda x: clean_answer(
                x,
                {
                    "1": "Ada Ciganlija",
                    "2": "Košutnjak",
                    "3": "Kalemegdan",
                },
            )
        )

        df = translate_answers(df=df, mappings=mapping)
        df = copy_demographics(df=df)
        df = df.assign(
            place_attachment=lambda x: x.filter(regex=r"8\.\d\s\w+").apply(
                lambda x: np.mean(
                    [
                        x.iloc[0],
                        x.iloc[1],
                        x.iloc[2],
                        x.iloc[3],
                        x.iloc[4],
                        x.iloc[5],
                    ]
                ),
                axis=1,
            ),
            social_cohesion=lambda x: x.filter(regex=r"9\.\d\s\w+").apply(
                lambda x: np.mean(
                    [x.iloc[0], x.iloc[1], 8 - x.iloc[2], 8 - x.iloc[3], x.iloc[4]]
                ),
                axis=1,
            ),
            accessibility=lambda x: x.filter(regex=r"10\.\d\s\w+").apply(
                lambda x: np.mean(x), axis=1
            ),
            sense_of_safety=lambda x: x.filter(regex=r"11\.\d\s\w+").apply(
                lambda x: np.mean(x), axis=1
            ),
            friendliness=lambda x: x.filter(regex=r"12\.\d\s\w+").apply(
                lambda x: np.mean(x), axis=1
            ),
            attractiveness=lambda x: x.filter(regex=r"13\.\d\s\w+").apply(
                lambda x: np.mean(x), axis=1
            ),
            quality_of_experience=lambda x: x["14 Quality of experience"],
            sense_of_space=lambda x: x.apply(
                lambda x: np.mean(x.loc["place_attachment":"social_cohesion"]), axis=1
            ),
            swls=lambda x: x.filter(regex=r"15\.\d\s\w+").apply(
                lambda x: np.sum(x), axis=1
            ),
            warwick_wellbeing=lambda x: x.filter(regex=r"16\.\d\s\w+").apply(
                lambda x: np.sum(x), axis=1
            ),
            ucla_loneliness=lambda x: x.filter(regex=r"17\.\d\s\w+").apply(
                lambda x: np.sum(x), axis=1
            ),
        )
        df.to_excel(PROC / f"{key}_cleaned.xlsx", index=False)


# %%
if __name__ == "__main__":
    main()

# %%
