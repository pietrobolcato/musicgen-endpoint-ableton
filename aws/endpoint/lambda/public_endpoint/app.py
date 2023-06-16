"""Lambda function allowing public access to the deployed endpoint"""

import os

import boto3
from botocore.config import Config
from chalice import Chalice
from sagemaker.deserializers import JSONDeserializer
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.session import Session

ENDPOINT_NAME = os.environ["ENDPOINT_NAME"]  # defined in `.chalice/config.json`

config = Config(read_timeout=30, retries={"max_attempts": 0})
sagemaker_runtime_client = boto3.client("sagemaker-runtime", config=config)
sagemaker_session = Session(sagemaker_runtime_client=sagemaker_runtime_client)

predictor = Predictor(
    endpoint_name=ENDPOINT_NAME,
    sagemaker_session=sagemaker_session,
    serializer=JSONSerializer(),
    deserializer=JSONDeserializer(),
)

app = Chalice(app_name="musicgen-public-endpoint")


@app.route("/", methods=["GET", "POST"])
def index():
    """Ping check"""
    return {"status": "online"}


@app.route("/inference", methods=["POST"])
def inference():
    """Perform inference with the deployed online endpoint"""
    response = predictor.predict(data=app.current_request.json_body)
    return response
