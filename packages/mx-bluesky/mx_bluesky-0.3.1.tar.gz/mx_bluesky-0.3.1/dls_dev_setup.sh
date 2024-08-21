#!/bin/bash

# controls_dev sets pip up to look at a local pypi server, which is incomplete
module unload controls_dev


module load python/3.11

if [ -d "./.venv" ]
then
rm -rf .venv
fi
mkdir .venv

python -m venv .venv
source .venv/bin/activate


pip install --upgrade pip
pip install wheel

pip install -e .[dev]

# Ensure we use a local version of dodal
if [ ! -d "../dodal" ]; then
  git clone git@github.com:DiamondLightSource/dodal.git ../dodal
fi

pip uninstall -y dodal
pip install -e ../dodal[dev]

tox -p
