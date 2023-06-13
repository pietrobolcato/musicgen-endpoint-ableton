#!/bin/bash
#shellcheck source=/dev/null
#shellcheck disable=SC2162

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Check if Python version is provided as command line argument
if [ -z "$1" ]
then
  # Prompt user for Python version if not provided
  read -p "+ Please enter Python version (e.g. 3.8): " python_version
else
  python_version="$1"
fi

echo "+ Creating conda environment called 'dev' with Python $python_version..."
conda create -n dev python="$python_version" -y
echo "+ Conda environment created!"

echo "+ Installing pip-tools..."
source activate dev
pip install pip-tools
echo "+ pip-tools installed!"

echo "+ Compiling requirements..."
bash "$SCRIPT_DIR/compile_requirements.sh"
echo "+ Requirements compiled!"

echo "+ Installing dev requirements..."
pip install -r "$SCRIPT_DIR/../requirements/dev.txt"
echo "+ Dev requirements installed!"

echo "+ All tasks completed!"
echo "+ To use the dev environment run: conda activate dev"