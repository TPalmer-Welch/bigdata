#!/usr/bin/env bash

set -e
source "venv/bin/activate"

python3 "find_lowest.py"

deactivate
