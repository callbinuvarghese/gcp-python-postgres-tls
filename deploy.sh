#!/bin/sh
set -x
gcloud run deploy $CLOUDRUN_SERVICE_NAME \
    --image=$CLOUDRUN_IMAGE_URL \
    --region $REGION \
    --platform=managed \
    --allow-unauthenticated  \
    --memory=2Gi \
    --set-env-vars NAME="Binu" \
    --set-env-vars DB_USER=$DB_USER \
    --set-env-vars DB_PASSWORD=$DB_PASSWORD \
    --set-env-vars DB_INSTANCE_IP="$DB_INSTANCE_IP" \
    --set-env-vars DB_INSTANCE_NAME="$DB_INSTANCE_NAME" \
    --set-env-vars DB_DATABASE="$DB_DATABASE" \
    --set-env-vars DB_SSL_MODE="$DB_SSL_MODE" \
    --vpc-connector $SERVERLESS_VPC_CONNECTOR \
    --project=$PROJECT_ID \
    --quiet