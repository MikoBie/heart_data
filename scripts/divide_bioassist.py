"""Script that aggregates data from Bioassist by questionnaire filled.
I make the assumption that the questionnaire was fille during the same
month.
"""

# %%
from heart import RAW, BIO
import json
import re
from tqdm import tqdm
from hashlib import md5
import os

# %%
rgx_prt = re.compile(r"\d*")
rgx_dt = re.compile(r"\d{4}-\d{2}")
rgx_vst = re.compile(r"^\d")
omt_lst = ["12344", "1234567890", "aATh9YF3DKqDBawx"]


# %%
def main() -> None:
    for item in tqdm(open(RAW / "bioassist.jsonl", "r")):
        item = json.loads(item)
        title = item["title"]
        part = rgx_prt.search(title).group()
        version = "first" if rgx_vst.search(title) else "final"
        created = item["createdAt"]
        created_simple = rgx_dt.search(created).group()
        user_id = item["userId"]
        file_name = md5(f"{user_id}_{created_simple}".encode()).hexdigest()
        answers = item["answers"]
        city = item["cityID"]
        tmp = {
            "user_id": user_id,
            "city": city,
            "created_at": created,
            "title": title,
            "part": part,
            "version": version,
            "answers": answers,
        }
        if user_id in omt_lst:
            continue
        if not os.path.exists(BIO / city.lower()):
            os.makedirs(BIO / city.lower())

        file_name = md5(f"{user_id}_{created_simple}_{version}".encode()).hexdigest()
        if city == "Aarhus":
            file_name = md5(f"{user_id}_{created_simple}".encode()).hexdigest()

        file = open(BIO / city.lower() / f"{file_name}.jsonl", "a")
        file.write(json.dumps(tmp) + "\n")
        file.close()


# %%
if __name__ == "__main__":
    main()
