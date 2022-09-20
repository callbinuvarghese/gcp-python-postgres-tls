#!/bin/sh

gcloud sql instances create $DB_INSTANCE_NAME \
    --project=$PROJECT_ID \
    --network=projects/$PROJECT_ID/global/networks/default \
    --no-assign-ip \
    --database-version=POSTGRES_13 \
    --cpu=2 \
    --memory=4GB \
    --region=$REGION \
    --root-password=${DB_INSTANCE_PASSWORD}

export DB_INSTANCE_IP=$(gcloud sql instances describe $DB_INSTANCE_NAME \
    --format=json | jq \
    --raw-output ".ipAddresses[].ipAddress")

gcloud sql users create ${DB_USER} \
    --password=$DB_PASSWORD \
    --instance=$DB_INSTANCE_NAME

gcloud sql databases create $DB_DATABASE --instance=$DB_INSTANCE_NAME

# After connection work from Private IP
gcloud sql instances patch $DB_INSTANCE_NAME --require-ssl

# Certs
gcloud beta sql ssl server-ca-certs list --instance="$DB_INSTANCE_NAME"

gcloud beta sql ssl server-ca-certs list \
--format="value(cert)" \
--instance="$DB_INSTANCE_NAME" > \
"./$DB_INSTANCE_NAME.cacert.pem"

➜   gcloud sql ssl client-certs list --instance="$DB_INSTANCE_NAME"
Listed 0 items.
➜   gcloud sql ssl client-certs create client-cert ./$DB_INSTANCE_NAME.client-key.pem --instance="$DB_INSTANCE_NAME"

NAME         SHA1_FINGERPRINT                          EXPIRATION
client-cert  6000e0d04d6b860fb044916482fb3b3e5b35f9a9  2032-09-16T15:39:25.050Z
➜   gcloud sql ssl client-certs list  --instance="$DB_INSTANCE_NAME"
NAME         SHA1_FINGERPRINT                          EXPIRATION
client-cert  6000e0d04d6b860fb044916482fb3b3e5b35f9a9  2032-09-16T15:39:25.050Z
➜   gcloud sql ssl client-certs describe client-cert  --instance="$DB_INSTANCE_NAME" --format="value(cert)" > ./$DB_INSTANCE_NAME.client-cert.pem


# psql "sslmode=verify-ca sslrootcert=server-ca.pem \
#      sslcert=client-cert.pem sslkey=client-key.pem \
#      hostaddr={IP_ADDRESS} \
#      port=5432 \
#      user=postgres dbname=postgres"

#chmod 0600 client-key.pem
#➜  openssl x509 -in client-cert.pem -out client-cert.crt
#➜  openssl x509 -in cacert.pem -out cacert.crt
