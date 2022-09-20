#!/bin/sh
set -x
export CLOUDRUN_SERVICE_URL=$(gcloud run services describe $CLOUDRUN_SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

#export BEARER_TOKEN=$(gcloud auth print-identity-token)
curl -X GET $CLOUDRUN_SERVICE_URL -H "Authorization: bearer $(gcloud auth print-identity-token)"
