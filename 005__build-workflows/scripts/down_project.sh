#!/bin/bash

# set login
./scripts/set_gcp_login.sh

# Load environment variables
env_file=".env"
source $env_file

DeleteServices() {
  # Dataset
  bq rm -r -f $DATASET

  # Cloud Function
  gcloud functions delete $FUNCTION_NAME --quiet

  # Cloud Run
  gcloud run services delete $IMAGE_NAME --region $REGION --quiet

  # Artifact Registry
  gcloud artifacts repositories delete $IMAGE_NAME --location $REGION --quiet

  # Workflows
  gcloud workflows delete $WORKFLOW_NAME --quiet

  # Cloud Buil Trigger
  gcloud builds triggers delete github $TRIGGER_NAME

  # Delete All Bucket
  gsutil rm -r -f $(gsutil ls)
}

DeleteServices
