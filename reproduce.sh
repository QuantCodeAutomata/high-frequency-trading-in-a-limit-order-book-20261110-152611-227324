#!/usr/bin/env bash
# Runs the test suite and all three experiments from the repository root.
set -eu

python -m pytest

python -m exp.exp1
python -m exp.exp2
python -m exp.exp3
