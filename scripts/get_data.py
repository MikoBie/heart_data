"""
Script to get data from the HEART API and save it to JSONL files.
"""

# %%
from heart.api import HEART


# %%
def main():
    heart = HEART()
    heart.connect()
    heart.write_out("bioassist.jsonl", endpoint="bioassist")
    heart.write_out("sentio.jsonl", endpoint="sentio")


# %%
if __name__ == "__main__":
    main()
# %%
