#!/bin/sh
set -x
gcloud builds submit --region=us-east4 --tag us-east4-docker.pkg.dev/$PROJECT_ID/quickstart-docker-repo/py-run-sql:latest
