"""Locust test for an AWS Sagemaker endpoint"""

import logging
import os
import time

import boto3
from botocore.config import Config
from locust import events, task
from locust.contrib.fasthttp import FastHttpUser

# constants
REGION = os.environ.get("REGION", "us-east-1")
CONTENT_TYPE = os.environ.get("CONTENT_TYPE", "application/json")
PAYLOAD_FILE = os.environ.get("PAYLOAD_FILE", "../payload/payload.json")

with open(PAYLOAD_FILE) as payload_file_handler:
    payload = payload_file_handler.read()


class BotoClient:
    """Main client class"""

    def __init__(self, host):
        logging.info(
            f"Initializing class with: \
            REGION = {REGION}, \
            CONTENT_TYPE = {CONTENT_TYPE}, \
            PAYLOAD_FILE = {PAYLOAD_FILE}",
        )

        config = Config(
            region_name=REGION,
            retries={"max_attempts": 0, "mode": "standard"},
        )

        with open(PAYLOAD_FILE) as payload_file_handler:
            payload = payload_file_handler.read()

        self.sagemaker_client = boto3.client("sagemaker-runtime", config=config)
        self.endpoint_name = host.split("/")[-1]
        self.content_type = CONTENT_TYPE
        self.payload = payload

    def send(self):
        request_meta = {
            "request_type": "InvokeEndpoint",
            "name": "SageMaker",
            "start_time": time.time(),
            "response_length": 0,
            "response": None,
            "context": {},
            "exception": None,
        }
        start_perf_counter = time.perf_counter()

        try:
            response = self.sagemaker_client.invoke_endpoint(
                EndpointName=self.endpoint_name,
                Body=self.payload,
                ContentType=self.content_type,
            )
            logging.info(response["Body"].read())
        except Exception as exception:
            request_meta["exception"] = exception

        request_meta["response_time"] = (
            time.perf_counter() - start_perf_counter
        ) * 1000

        events.request.fire(**request_meta)


class BotoUser(FastHttpUser):
    """BotoUser class, super class of `MyUser`"""

    abstract = True

    def __init__(self, env):
        super().__init__(env)
        self.client = BotoClient(self.host)


class MyUser(BotoUser):
    """Actual user class"""

    @task
    def send_request(self):
        self.client.send()
