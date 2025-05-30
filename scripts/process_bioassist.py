"""Script that converts JSON line files into a long format excell files."""

# %%
from heart import BIO
from heart.mappings import (
    belgrade_q_dct,
    athens_q_dct,
    aarhus_q_dct,
    questionnaire_final,
    questionnaire_first,
)
from heart.utils import extract_value
import json
import pandas as pd
import os
import re
from tqdm import tqdm

# %%
lst_athens = [item for item in os.scandir(BIO / "athens") if "jsonl" in item.name]
lst_aarhus = [item for item in os.scandir(BIO / "aarhus") if "jsonl" in item.name]
lst_belgrade = [item for item in os.scandir(BIO / "belgrade") if "jsonl" in item.name]
translate_dct = {
    "Aarhus": aarhus_q_dct,
    "Belgrade": belgrade_q_dct,
    "Athens": athens_q_dct,
}
questionnaire_first_reversed = {v: k for k, v in questionnaire_first.items()}
rgx = re.compile(r"\d*(\.\d+)?")


# %%
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
                    response=lambda x: x["value"].apply(lambda y: extract_value(y))
                )
                part["question"] = part["questionTitle"].apply(
                    lambda x: rgx.search(x).group() if rgx.search(x) else x.strip()
                )
                part["version"] = line["version"]
                part["city"] = line["city"]
                part["user_id"] = line["user_id"]
                part["created_at"] = line["created_at"]
                part["part"] = line["part"]
                questionnaire = pd.concat([questionnaire, part])
            if questionnaire.empty:
                continue
            version = questionnaire["version"].iloc[0]
            city = questionnaire["city"].iloc[0]
            if version == "first":
                questionnaire["question_eng"] = questionnaire["question"].map(
                    questionnaire_first
                )
            else:
                questionnaire["question_eng"] = questionnaire["question"].map(
                    questionnaire_final
                )
            questionnaire["question_eng"] = (
                questionnaire["questionTitle"]
                .map(translate_dct[city])
                .fillna(questionnaire["question_eng"])
            )
            questionnaire["question_eng"] = questionnaire["question_eng"].map(
                lambda x: questionnaire_first_reversed.get(x, "") + " " + x
            )

            questionnaire = questionnaire[
                [
                    "user_id",
                    "created_at",
                    "city",
                    "version",
                    "question_eng",
                    "response",
                    "questionTitle",
                ]
            ]
            file_path = item.path.replace("jsonl", "xlsx")
            questionnaire.sort_values("created_at", ascending=True).drop_duplicates(
                "question_eng", keep="last"
            ).to_excel(file_path, index=False)


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
