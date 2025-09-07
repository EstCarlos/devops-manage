#!/bin/bash

# Ensure the script stops if an error occurs
set -e

# Phase: Install
echo "BUILD PHASE HAS STARTED"

# Ensure Python is installed
# This step depends on your system's configuration.
# For Ubuntu, you might use `update-alternatives` or `pyenv`

# Phase: Pre-build
pip install --upgrade pip
pip install -r requirements-dev.txt -t ./dependencies/python

# Clean up Python bytecode and metadata
cd ./dependencies/python
rm -rf *dist-info __pycache__
find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
cd ../../

# Check if a Python virtual environment is already active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "No virtual environment detected. Setting up a new one."
    # Create a Python virtual environment if not already activated
    python3 -m venv .venv
    # Activate the virtual environment
    source .venv/bin/activate
else
    echo "A virtual environment is already active: $VIRTUAL_ENV"
fi

pip install -r ./requirements.txt
pip install -r ./requirements-dev.txt


