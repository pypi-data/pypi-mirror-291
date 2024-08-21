#!/bin/bash -eux
rm -rf dist/*
nano pyproject.toml
python -m build
python3 -m twine upload dist/*
python -m build
