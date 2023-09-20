#!/bin/bash

# -----------------------------------------------------------------------------------------
# Documentation here...
# -----------------------------------------------------------------------------------------

# set login
./scripts/gcp_login.sh

# Set environment variables using the .env file
env_file=".env"
source $env_file


# Publish message on Pub/Sub
gcloud pubsub topics publish $TOPIC_NAME --message='{"id": "uuidgen","message":"0400 trigger-sdk-to-pub/sub"}'

# Publish message on Cloud Run
curl -X 'POST' \
  'https://image-project-005-55nsgsicwq-uc.a.run.app/v1/logs/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"message": "0400 trigeer-sdk-to-cloud-run"}'

# Publish message on Cloud Functions
curl -X 'POST' \
  'https://us-central1-fine-sublime-315119.cloudfunctions.net/function_project_005' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '0400 trigger-sdk-to-functions'
