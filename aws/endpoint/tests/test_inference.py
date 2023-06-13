"""Test scoring script functions"""

import sys
from pathlib import Path

ENDPOINT_SRC_ROOT_DIR = Path(__file__).parents[1].resolve() / "src"
sys.path.append(str(ENDPOINT_SRC_ROOT_DIR))

import pytest

import aws.endpoint.src.code.inference as inference
import aws.endpoint.tests.utils as aws_tests_utils

# to fill
