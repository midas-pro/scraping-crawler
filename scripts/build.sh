#!/bin/bash

VERSION=$(head -n 1 src/VERSION)

PY="python3"
PIP="$PY -m pip --disable-pip-version-check"

rm -rf venv build dist *.egg-info

$PY -m venv venv
. venv/bin/activate

$PIP install -U pip==20.0.2
$PIP install -U setuptools wheel

$PIP install PyInstaller cairosvg
$PIP install -r requirements.txt

$PY setup.py clean bdist_wheel sdist package

deactivate
rm -rf venv build *.egg-info

# FINISHED
