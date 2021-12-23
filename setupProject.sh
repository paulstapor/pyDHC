#!/bin/bash

# set variables
PYDHC_VENV="pyDhcVenv"
PYDHC_DIR="$(cd "$(dirname "$1")"; pwd -P)/$(basename "$1")";
# create the environment
python3 -m venv "$PYDHC_DIR/$PYDHC_VENV"

# activate it and install requirements
source $PYDHC_VENV/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# create a shortcut for activating the venv
ln -s "$PYDHC_DIR/$PYDHC_VENV/bin/activate" dhcVenv

# generate the run configuration
mkdir .idea
mkdir .idea/runConfigurations
cp runconfigurations .idea/runConfigurations/pyDHC.xml

