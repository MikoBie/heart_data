# `HEART`

Scripts to extract data from from the HEART database and convert them to a wide format.

## Main dependencies

* _python3.9_ ([anaconda distribution](https://www.anaconda.com/products/distribution) is preferred)
* other _python_ dependencies are specified in `environment.yaml`

## Setup

1. Clone the repo: git@github.com:MikoBie/heart_data.git.
2. Set up the proper virtual environment.
```bash
cd heart_data
conda env create --file environment.yaml
```
3. Set up the environment variables.
```bash
cd $CONDA_PREFIX
mkdir -p etc/conda/activate.d
mkdir -p etc/conda/deactivate.d
touch etc/conda/activate.d/env_vars.sh
touch etc/conda/deactivate.d/env_vars.sh
```
`activate.d/env_vars.sh` should look more or less like the following:
```bash
#!/bin/sh
export heart_username=<value>
export heart_password=<value>
```
`deactivate.d/env_vars.sh` should look more or less like the following:
```bash
#!/bin/sh
unset heart_username
unset heart_password
```
4. Activate `pre-commit`.
```bash
pre-commit install
```
5. Cross fingers.

## Running

In general, the scripts are run from the command line but you can also run them in interactive mode in Visual Studio Code. The scripts are located in the `scripts` folder. They should be run in the following order:
```bash
python scripts/get_data.py ## Gets the data from the database thourgh the API
python scripts/divide_bioassist.py ## Divides the data into files. Each quesitonnaire is saved in a separate file.
python scripts/process_bioassist.py ## Processes the data and saves it xlsx files.
python scripts/merge_excels.py ## Merge excels into an excel per city.
```
