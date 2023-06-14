"""Download musicgen model artifacts"""

import glob
import logging
import os
import shutil

from audiocraft.models import musicgen

# define logging settings
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main() -> None:
    """Downloads the models and move them to the artifacts folder"""
    logging.info("Downloading models...")
    musicgen.MusicGen.get_pretrained("medium", device="cuda")

    # move models to the artifacts folder
    file_dir_base_path = os.path.dirname(os.path.realpath(__file__))

    for file in glob.glob(os.path.expanduser("~/.cache/torch/hub/checkpoints/*.th")):
        file_name = os.path.basename(file)
        dest_artifacts_file_full_path = os.path.join(file_dir_base_path, file_name)

        logging.info(f"Moving {file} to {dest_artifacts_file_full_path}")
        shutil.move(file, dest_artifacts_file_full_path)

    logging.info("Done")


if __name__ == "__main__":
    """Script entrypoint"""
    main()
