#!/bin/bash
#shellcheck disable=SC2162
#shellcheck disable=SC1091

# This script exports the dev and prod environment to a conda YAML file that can be used to re-create them.
# The `dev` environment initialized with the `init.sh` must be present beforehand to determine the right python version
#
# Usage:
#   ./conda_export.sh. The script will automatically create two Conda environments and export them to YAML files.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DEV_PYTHON_VERSION=$(source activate dev && python --version 2>&1 | awk '{print $2}')

export_conda_env() {
  local env_name="$1"
  local random_id=temp_$RANDOM

  echo "+ Creating a temporary conda environment called $random_id with Python $DEV_PYTHON_VERSION..."
  conda create --name $random_id python="$DEV_PYTHON_VERSION" -y
  echo "+ Conda environment created!"

  echo "+ Installing $env_name requirements..."
  source activate $random_id
  pip install -r "$SCRIPT_DIR/../requirements/$env_name.txt"
  echo "+ Requirements installed!"

  echo "+ Exporting $env_name environment..."
  conda env export > "$SCRIPT_DIR/../envs/$env_name.yaml"
  sed -i "s/$random_id/$env_name/g" "$SCRIPT_DIR/../envs/$env_name.yaml"
  echo "+ Environment exported!"

  echo "+ Cleaning up..."
  conda deactivate
  conda env remove --name $random_id -y
  echo "+ Done!"
}

export_conda_env "dev"
export_conda_env "prod"

echo "Environment files are saved in: $SCRIPT_DIR/../requirements/"