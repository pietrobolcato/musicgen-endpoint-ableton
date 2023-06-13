#!/bin/bash
# this scripts runs the first time setup in the dev container

# setup pre-commit
pre-commit install --install-hooks
pre-commit run --all-files