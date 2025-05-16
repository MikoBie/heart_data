"""Script that converts JSON line files into a long format excell files."""

# %%
from heart import BIO
from heart.mappings import questions_dct, belgrade_q_dct, athens_q_dct, aarhus_q_dct
import json
import pandas as pd
import os
import re
from tqdm import tqdm

pd.set_option("future.no_silent_downcasting", True)

# %%
lst_athens = [item for item in os.scandir(BIO / "athens") if "jsonl" in item.name]
lst_aarhus = [item for item in os.scandir(BIO / "aarhus") if "jsonl" in item.name]
lst_belgrade = [item for item in os.scandir(BIO / "belgrade") if "jsonl" in item.name]
translate_dct = {
    "Aarhus": aarhus_q_dct,
    "Belgrade": belgrade_q_dct,
    "Athens": athens_q_dct,
}
rgx = re.compile(r"\d*(\.\d+)?")


# %%
def extract_value(dct: dict) -> str:
    """Extract the value of the answers.

    Parameters
    ----------
    dct : dict
        a dictionary with fields, body, selectionId, score.

    Returns
    -------
    str
        a selected answer, either an integer or description.
    """
    return dct["selectionId"] if dct["selectionId"] else ", ".join(dct["body"])


def produce_excells(lst_fls: list) -> None:
    """Takes a list of JSON lines files and converts them into a excel files. On the
    fly it converts them into a long format. Each row represents an answer to the
    question.

    Parameters
    ----------
    lst_fls : list
        a list of DirEntries JSON line files.
    """
    for item in tqdm(lst_fls):
        with open(item, "r") as file:
            questionnaire = pd.DataFrame()
            for line in file.readlines():
                line = json.loads(line)
                if not line["answers"]:
                    continue
                part = pd.DataFrame.from_dict(line["answers"]).assign(
                    question=lambda x: x["questionTitle"].apply(
                        lambda y: rgx.search(y).group()
                    ),
                    response=lambda x: x["value"].apply(lambda y: extract_value(y)),
                    user_id=line["user_id"],
                    created_at=line["created_at"],
                    title=line["title"],
                    part=line["part"],
                    city=line["city"],
                )[
                    [
                        "user_id",
                        "created_at",
                        "city",
                        "title",
                        "part",
                        "questionTitle",
                        "question",
                        "response",
                    ]
                ]
                questionnaire = pd.concat([questionnaire, part])
            file_path = item.path.replace("jsonl", "xlsx")
            if questionnaire.empty:
                continue
            for city, translation in translate_dct.items():
                if city in questionnaire["city"].unique():
                    questionnaire["question_eng"] = questionnaire["question"].map(
                        questions_dct
                    )
                    questionnaire["question_eng"] = (
                        questionnaire["questionTitle"]
                        .map(translation)
                        .fillna(questionnaire["question_eng"])
                    )
            questionnaire.sort_values(
                axis=0, ascending=True, by="created_at"
            ).reset_index().drop(["index"], axis="columns").to_excel(file_path)


def main() -> None:
    print("Process data from Athens")
    produce_excells(lst_athens)
    print("Process data from Belgrade")
    produce_excells(lst_belgrade)
    print("Process data from Aarhus")
    produce_excells(lst_aarhus)


# %%
if __name__ == "__main__":
    main()

# %%
