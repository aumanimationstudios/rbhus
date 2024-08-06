#!/usr/bin/env bash
rm -rf rbhus-env
python3 -m venv rbhus-env
source rbhus-env/bin/activate
unset PYTHONPATH
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "----- Created venv -------"
