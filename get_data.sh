#!/usr/bin/env bash
## Naive way of running all scripts.

python scripts/get_data.py
python scripts/divide_bioassist.py
python scripts/process_bioassist.py
python scripts/merge_excels.py
python scripts/clean_answers.py
