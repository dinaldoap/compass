#!/bin/bash

# Create virtual environment and install dependencies
python -m venv --clear --prompt=compass .venv
source .venv/bin/activate
make install
