#!/bin/bash

# -----------------------------------------------------------------------------------------
# Documentation here...
# -----------------------------------------------------------------------------------------

# set login
./scripts/gcp_login.sh

# Set environment variables using the .env file
env_file=".env"
source $env_file


# # Publish message on Pub/Sub
# gcloud pubsub topics publish $TOPIC_NAME --message='{"id": "uuidgen","message":"07:41"}'

# # Publish message on Cloud Run
# # 'https://image-project-005-55nsgsicwq-uc.a.run.app/v1/logs/' \
# curl -X 'POST' \
#   'http://localhost:8080/v1/logs/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{"message": "7:52"}'

# # Publish message on Cloud Functions
# curl -X 'POST' \
#   'http://localhost:8080/v1/logs/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '7:52'
