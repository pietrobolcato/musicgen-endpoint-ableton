#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

rm -rf "$SCRIPT_DIR"/../requirements/prod.txt
rm -rf "$SCRIPT_DIR"/../requirements/dev.txt
rm -rf "$SCRIPT_DIR"/../requirements/chalice.txt

pip-compile "$SCRIPT_DIR"/../requirements/prod.in --resolver=backtracking
pip-compile "$SCRIPT_DIR"/../requirements/dev.in --resolver=backtracking
pip-compile "$SCRIPT_DIR"/../requirements/chalice.in --resolver=backtracking