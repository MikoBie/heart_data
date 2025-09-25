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

## Preprocessing

In general, the scripts are run from the command line but you can also run them
in interactive mode in Visual Studio Code. The scripts are located in the
`scripts` folder. To run all the preprocessing steps it is enough to run the
following bash script from the root of the repository. It will create a `data`
folder in the root of the repository and run all the scripts in the correct
order.

```bash
bash get_data.sh
```

## Analysis

The analysis scripts are located in the `scripts` folder. They should be in the
interactive mode in Visual Studio Code. Their names should be self-explanatory
since they start with the name of the city and then describe part of the
questionnaire. For example, `belgrade_demographics.py` contains the code to
process the demographics part of the questionnaire for Belgrade.

## Funding

This project has received funding from the European Union’s Horizon 2020
Research and Innovation Program under grant agreement No 945105.
