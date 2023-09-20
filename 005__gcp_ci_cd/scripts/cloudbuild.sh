#!/bin/bash

# --------------------------------------------------------------------------
# Deploy Script Documentation
# --------------------------------------------------------------------------

# This script automates the deployment of various components of a cloud
# application, including a workflow, Cloud Storage files, BigQuery statements,
# a Cloud Run service, and a Cloud Function.

# Usage:
#   Run this script to deploy the specified components. Ensure that the
#   necessary environment variables are set and correctly configured before
#   executing the script.

# Note:
#   - The script deploys the following components:
#     - Workflows defined in a YAML file.
#     - Copies files to Google Cloud Storage.
#     - Deploys BigQuery SQL statements.
#     - Builds and deploys a Docker image to Cloud Run.
#     - Deploys a Cloud Function.

#   - Ensure that the gcloud CLI is installed and configured with the necessary
#     permissions and project settings before running the script.

#   - Set the appropriate environment variables like WORKFLOW_NAME, BUCKET_NAME,
#     PROJECT, REGION, IMAGE_NAME, FUNCTION_NAME, TOPIC_NAME, and CLOUD_RUN_URL
#     to match your project's configuration.

#   - Modify the script as needed to suit your specific deployment requirements.

#   - Run the script with appropriate permissions to ensure successful
#     deployment of your application components.
# --------------------------------------------------------------------------

FOLDER='.'

# Deploy workflow.yaml
gcloud workflows deploy $WORKFLOW_NAME \
  --source $FOLDER/workflows/$WORKFLOW_NAME.yaml \
  --set-env-vars TOPIC_NAME=$TOPIC_NAME,CLOUD_RUN_URL=$CLOUD_RUN_URL,FUNCTION_URL=$FUNCTION_URL

# Copy files to Cloud Storage
gsutil cp $FOLDER/storage/* gs://$BUCKET_NAME/storage/

# Deploy Bigquery Statements
sed -e 's/<PROJECT>/' $PROJECT/g -e s/<DATASET>/$DATASET'/g' $FOLDER/database/*.sql | bq query --nouse_legacy_sql

# Deploy Cloud Run Service
## Build Image
docker build -t $REGION-docker.pkg.dev/$PROJECT/$IMAGE_NAME/api $FOLDER/api/.

## Configure authentication
gcloud auth configure-docker $REGION-docker.pkg.dev

## Push Image to artifacts repositories
docker push $REGION-docker.pkg.dev/$PROJECT/$IMAGE_NAME/api

## Run Service
gcloud run deploy $IMAGE_NAME \
  --image $REGION-docker.pkg.dev/$PROJECT/$IMAGE_NAME/api \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated

# Deploy Cloud Function
gcloud functions deploy $FUNCTION_NAME \
  --runtime python310 \
  --source $FOLDER/function/ \
  --entry-point trigger \
  --region $REGION \
  --set-env-vars TOPIC_NAME=$TOPIC_NAME,CLOUD_RUN_URL=$CLOUD_RUN_URL \
  --trigger-http \
  --allow-unauthenticated
