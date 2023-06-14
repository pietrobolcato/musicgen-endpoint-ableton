#!/bin/bash
# build and push the docker image
ECR_LINK="138140302683.dkr.ecr.us-east-1.amazonaws.com"
IMAGE_NAME="musicgen-pytorch:1.0"

docker build -t "$IMAGE_NAME" -t "$ECR_LINK"/"$IMAGE_NAME" .
docker push "$ECR_LINK"/"$IMAGE_NAME"