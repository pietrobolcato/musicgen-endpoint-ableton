#!/bin/bash
# build and push the docker image
ECR_URL="138140302683.dkr.ecr.us-east-1.amazonaws.com"
IMAGE_NAME="musicgen-pytorch:1.0"
REGION="us-east-1"

# login
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$ECR_URL"

# build and publish
docker build -t "$IMAGE_NAME" -t "$ECR_URL"/"$IMAGE_NAME" .
docker push "$ECR_URL"/"$IMAGE_NAME"