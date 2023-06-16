"""Test scoring script functions"""

import sys
from pathlib import Path

ENDPOINT_SRC_ROOT_DIR = Path(__file__).parents[1].resolve() / "src"
sys.path.append(str(ENDPOINT_SRC_ROOT_DIR))

import json

import pytest
from audiocraft.models import musicgen
from pydantic import ValidationError

import aws.endpoint.src.code.inference as inference


def run_inference(request_body: dict, model: musicgen.MusicGen) -> dict:
    """
    Runs inference

    Parameters
    ----------
    request_body : dict
        The request parameters
    model : musicgen.MusicGen
        The loaded musicgen model

    Returns
    -------
    dict
        The inference output
    """
    validated_model = inference.input_fn(
        request_body=json.dumps(request_body),
        content_type="application/json",
    )
    prediction = inference.predict_fn(validated_model=validated_model, model=model)

    output = inference.output_fn(prediction=prediction, content_type="application/json")
    return output


@pytest.fixture()
def model():
    """Loads the pre-trained model"""
    model = inference.model_fn(model_dir=ENDPOINT_SRC_ROOT_DIR)
    return model


def test_valid_request(model):
    """Tests a valid request"""
    request_body = {
        "prompt": "berghain acid techno",
        "duration": 1,
        "temperature": 1.0,
        "top_p": 0.0,
        "top_k": 250,
        "cfg_coefficient": 3.0,
    }

    output = run_inference(request_body, model)

    assert "result" in output
    assert "prediction" in output["result"]
    assert "processing_time_ms" in output["result"]


def test_invalid_request(model):
    """Test an invalid request, missing the `prompt` parameter"""
    request_body = {
        "duration": 1,
        "temperature": 1.0,
        "top_p": 0.0,
        "top_k": 250,
        "cfg_coefficient": 3.0,
    }

    with pytest.raises(ValidationError):
        run_inference(request_body, model)
