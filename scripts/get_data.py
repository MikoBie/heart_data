"""
Script to get data from the HEART API and save it to JSONL files.
"""

# %%
from heart.api import HEART
import os

# %%
username = os.environ.get("heart_username")
password = os.environ.get("heart_password")


# %%
def main():
    heart = HEART()
    heart.connect_api(username=username, password=password)
    heart.write_out("bioassist.jsonl", endpoint="bioassist")
    heart.write_out("sentio.jsonl", endpoint="sentio")


# %%
if __name__ == "__main__":
    main()
# %%
