#!/bin/bash
# build and push the docker image
PUBLIC_ECR_LINK="public.ecr.aws/s0f8z6e9"
IMAGE_NAME="musicgen-pytorch:1.0"

docker build -t "$IMAGE_NAME" -t "$PUBLIC_ECR_LINK"/"$IMAGE_NAME" .
docker push "$PUBLIC_ECR_LINK"/"$IMAGE_NAME"