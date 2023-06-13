"""Test scoring script functions"""

import sys
from pathlib import Path

ENDPOINT_SRC_ROOT_DIR = Path(__file__).parents[1].resolve() / "src"
sys.path.append(str(ENDPOINT_SRC_ROOT_DIR))

import json

import aws.endpoint.src.code.inference as inference

# import pytest

# import aws.endpoint.tests.utils as aws_tests_utils

request_body = json.dumps(
    {
        "prompt": "berghain acid techno",
        "duration": 1,
        "temperature": 1.0,
        "top_p": 0.0,
        "top_k": 250,
        "cfg_coefficient": 3.0,
    },
)

model = inference.model_fn(model_dir=ENDPOINT_SRC_ROOT_DIR)
input_data = inference.input_fn(
    request_body=request_body,
    content_type="application/json",
)
prediction = inference.predict_fn(input_data=input_data, model=model)
output = inference.output_fn(prediction=prediction, content_type="application/json")
