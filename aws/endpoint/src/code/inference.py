"""Inference code for the model"""

import logging
import time
from typing import Any

import torch
from helpers import helpers

# define logging settings
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def model_fn(model_dir: str) -> Any:
    """Loads the models"""
    logging.info(f"CUDA available: {torch.cuda.is_available()}")
    logging.info("Loading the model...")
    start_time = time.time()

    model = None  # fill this

    end_time = time.time()
    logging.info(f"Model loading completed in {(end_time - start_time):.2f} seconds")

    return model


def predict_fn(input_data: bytes, model: Any) -> dict:
    """Perform inference based on the request"""
    start_time = time.time()

    logging.info(f"Received request with data: {input_data}")

    result = None  # fill this

    end_time = time.time()
    processing_time_ms = int((end_time - start_time) * 1000)

    return {
        "result": {"prediction": result, "processing_time_ms": processing_time_ms},
    }
