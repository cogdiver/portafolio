#!/bin/bash

# -----------------------------------------------------------------------------------------
# Script to automate the setup of a Google Cloud Platform (GCP) project configuration.
# This script offers a range of options such as enabling APIs, creating essential services,
# and adding required permissions to the GCP project. It streamlines the setup process,
# ensuring that necessary components are in place for effective project development
# and deployment. Usage of the script simplifies the initial GCP configuration, making
# it suitable for development, testing, and CI/CD workflows.
# -----------------------------------------------------------------------------------------

# set login
./scripts/gcp_login.sh

# Set environment variables using the .env file
env_file=".env"
source $env_file


EnableAPIs() {
    gcloud services enable dataflow.googleapis.com
    gcloud services enable datapipelines.googleapis.com
    gcloud services enable cloudscheduler.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable cloudfunctions.googleapis.com
    gcloud services enable secretmanager.googleapis.com
    # gcloud services enable secretmanager.googleapis.com
}

CreateServices() {
    # Cloud Buil (Trigger)
    gcloud builds triggers create github \
        --name=$TRIGGER_NAME \
        --repo-name=$GITHUB_REPO_NAME \
        --repo-owner=$GITHUB_REPO_OWNER \
        --branch-pattern=$BRANCH_PATTERN \
        --build-config=$FOLDER/cloudbuild.yaml \
        --substitutions=_FOLDER="$FOLDER",_WORKFLOW_NAME="$WORKFLOW_NAME",_BUCKET_NAME="$BUCKET_NAME",_PROJECT="$PROJECT",_IMAGE_NAME="$IMAGE_NAME",_REGION="$REGION",_FUNCTION_NAME="$FUNCTION_NAME",_DATASET="$DATASET",_TOPIC_NAME="$TOPIC_NAME",_CLOUD_RUN_URL="$CLOUD_RUN_URL",_FUNCTION_URL="$FUNCTION_URL"

    # Storage (Bucket)
    gsutil mb gs://$BUCKET_NAME

    # Bigquery (Dataset)
    bq mk -f $DATASET

    # Artifact Registry (Repository)
    gcloud artifacts repositories create $IMAGE_NAME \
        --repository-format=docker \
        --location=$REGION

    # Pub/Sub (Topic, Subscription)
    gcloud pubsub topics create $TOPIC_NAME
    gcloud pubsub subscriptions create $SUBSCRIPTION_NAME --topic $TOPIC_NAME
    gcloud pubsub subscriptions create $SUBSCRIPTION_NAME-test --topic $TOPIC_NAME

    # Dataflow (Template)
    gcloud dataflow jobs run $JOB_NAME \
        --gcs-location gs://dataflow-templates-$REGION/latest/PubSub_Subscription_to_BigQuery \
        --region $REGION \
        --staging-location gs://$BUCKET_NAME/temp/ \
        --parameters inputSubscription=projects/$PROJECT/subscriptions/$SUBSCRIPTION_NAME,javascriptTextTransformGcsPath=gs://$BUCKET_NAME/storage/udf.js,javascriptTextTransformFunctionName=process,outputTableSpec=$PROJECT:$DATASET.logs,outputDeadletterTable=$PROJECT:$DATASET.errors

    # Execute trigger
    gcloud builds triggers run $TRIGGER_NAME --branch=$BRANCH_PATTERN
}

AddPermissions() {
    # Set permissions
    PROJECT_NUMBER=`gcloud projects describe $PROJECT --format='value(projectNumber)'`

    # To execute workflow from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/workflows.admin \
        --condition=None &> /dev/null

    # To execute bigquery queries from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/bigquery.admin \
        --condition=None &> /dev/null

    # To deploy Cloud Run services from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/run.admin \
        --condition=None &> /dev/null
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/run.serviceAgent \
        --condition=None &> /dev/null

    # To deploy Cloud Function from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/cloudfunctions.admin \
        --condition=None &> /dev/null

    # To write pub/sub message on bigquery
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com \
        --role=roles/bigquery.admin \
        --condition=None &> /dev/null
}

EnableAPIs
CreateServices
AddPermissions

echo "-------------------------"
echo "|    Setup completed    |"
echo "-------------------------"
