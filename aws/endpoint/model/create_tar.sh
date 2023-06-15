#!/bin/bash
# creates the `model.tar.gz` file with the right folder structure

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
src_root_folder="../src/"

CODE_FOLDER="code"
HELPERS_FOLDER="helpers"
ARTIFACTS_FOLDER="artifacts"

cd $src_root_folder || exit
tar cvf "$script_dir"/model.tar.gz --use-compress-program=pigz $CODE_FOLDER $HELPERS_FOLDER $ARTIFACTS_FOLDER