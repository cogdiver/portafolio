#!/bin/bash

# --------------------------------------------------------------------------
# This script demonstrates publishing messages to different Google Cloud
# services such as Pub/Sub, Cloud Run, and Cloud Functions based on the
# specified message type.
# --------------------------------------------------------------------------

# Load environment variables from the .env file
source .env

# Function to publish a message to Pub/Sub
publish_to_pubsub() {
    local message="$1"
    gcloud pubsub topics publish $TOPIC_NAME --message='{"id": "'$(uuidgen)'", "message": "'$message'"}'
}

# Function to publish a message to Cloud Run
publish_to_cloud_run() {
  local message="$1"
  curl -X POST "$CLOUD_RUN_URL/v1/logs/" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d "{\"message\": \"$message\"}"
}

# Function to publish a message to Cloud Functions
publish_to_cloud_functions() {
  local message="$1"
  local type="$2"
  curl -X POST $FUNCTION_URL \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"message": "'$message'", "type": "'$type'"}'
}

# Check if the required number of arguments are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 <service> <message>"
  exit 1
fi

service="$1"
message="$2"
type="$3"

# Execute the corresponding action based on the specified type
case "$service" in
  "pubsub") publish_to_pubsub "$message" ;;
  "cloud_run") publish_to_cloud_run "$message" ;;
  "cloud_functions") publish_to_cloud_functions "$message" "$type" ;;
  *)
    echo "Invalid type. Supported services are: pubsub, cloud_run, cloud_functions."
    exit 1
    ;;
esac
