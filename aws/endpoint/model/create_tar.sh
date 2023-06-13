#!/bin/bash

# This script creates the `model.tar.gz` file with the right folder structure

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Change the following variables as needed
# All the paths are relative to `SRC_ROOT_FOLDER`

SRC_ROOT_FOLDER="../src/"

CODE_FOLDER="code"
HELPERS_FOLDER="helpers"
LIBS_FOLDER="../../../src/ai_module_template/" # the model artifacts are also included here

cd $SRC_ROOT_FOLDER || exit
tar cvf "$script_dir"/model.tar.gz --use-compress-program=pigz $CODE_FOLDER $HELPERS_FOLDER $LIBS_FOLDER