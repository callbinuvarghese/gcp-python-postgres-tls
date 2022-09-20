#!/bin/sh
set -x
export DB_INSTANCE_NAME=binu-pg13
export DB_INSTANCE_PASSWORD=password123
export DB_DATABASE=test-db
export DB_USER=test-user
export DB_PASSWORD=testpassword123
export DB_SSL_MODE=verify_full

export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
export PROJECT_NAME=$(gcloud projects describe $PROJECT_ID --format='value(name)')
export REGION=us-east4

export CLOUDRUN_SERVICE_NAME=py-run-sql
export CLOUDRUN_IMAGE_NAME=us-east4-docker.pkg.dev/$PROJECT_ID/quickstart-docker-repo/py-run-sql:latest

export SERVERLESS_VPC_CONNECTOR=cymbalconnector
