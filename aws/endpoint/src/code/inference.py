"""Inference code for the model"""

import json
import logging
import os
import time

import torch
from audiocraft.models import musicgen
from helpers import utils
from helpers.schema.request import RequestModel

# define logging settings
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def model_fn(model_dir: str) -> musicgen.MusicGen:
    """
    Loads the model

    Parameters
    ----------
    model_dir : str
        The root path of the model, i.e. the root path of the tar.gz file

    Returns
    -------
    musicgen.MusicGen
        The loaded musicgen model
    """
    logging.info(f"CUDA available: {torch.cuda.is_available()}")
    logging.info("Loading the model...")
    start_time = time.time()

    # set paths for model loading
    os.environ["MUSICGEN_ROOT"] = os.path.join(model_dir, "artifacts/")
    model = musicgen.MusicGen.get_pretrained("medium", device="cuda")

    end_time = time.time()
    logging.info(f"Model loading completed in {(end_time - start_time):.2f} seconds")

    return model


def input_fn(request_body: str, content_type: str) -> RequestModel:
    """
    Preprocess the input data. Checks that its in json format, and returns a python
    dictionary

    Parameters
    ----------
    request_body : str
        The body of the request
    content_type : str
        The content type of the request

    Returns
    -------
    RequestModel
        The validated request model
    """
    assert content_type == "application/json", "Only `application/json` is supported"
    assert isinstance(request_body, str), "Expected `request_body` to be string"

    # validate request schema
    request_body = json.loads(request_body)
    validated_model = RequestModel(**request_body)

    return validated_model


def predict_fn(validated_model: RequestModel, model: musicgen.MusicGen) -> tuple:
    """
    Perform inference based on the request

    Parameters
    ----------
    validated_model : RequestModel
        The validated request input data, returned by the `input_fn` function
    model : musicgen.MusicGen
        The musicgen loaded model

    Returns
    -------
    tuple
        A tuple containing the output audio in base64 encoded string, and the processing
        time
    """
    start_time = time.time()
    logging.info(f"Received request with data: {validated_model}")

    # set generation parameters
    model.set_generation_params(
        duration=validated_model.duration,
        temperature=validated_model.temperature,
        top_p=validated_model.top_p,
        top_k=validated_model.top_k,
        cfg_coef=validated_model.cfg_coefficient,
    )

    # run prediction
    prediction = model.generate([validated_model.prompt], progress=False)

    # convert prediction to base64
    prediction_base64 = utils.audio_to_base64(
        audio=prediction[0],
        sample_rate=model.sample_rate,
    )

    end_time = time.time()
    processing_time_ms = int((end_time - start_time) * 1000)

    return prediction_base64, processing_time_ms


def output_fn(prediction: tuple, content_type: str) -> dict:
    """
    Returns the prediction of `predict_fn` in JSON format

    Parameters
    ----------
    prediction : tuple
        The prediction returned from the `predict_fn` function
    content_type : str
        The request output content type

    Returns
    -------
    dict:
        The output json in dictionary format
    """
    assert content_type == "application/json", "Only `application/json` is supported"

    logging.info("Output function called")
    logging.info(f"Content type: {content_type}")

    prediction_base64, processing_time_ms = prediction

    return {
        "result": {
            "prediction": prediction_base64,
            "processing_time_ms": processing_time_ms,
        },
    }
