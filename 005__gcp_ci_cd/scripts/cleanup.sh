#!/bin/bash

# --------------------------------------------------------------------------
# Script for cleaning up resources in a Google Cloud Platform (GCP) project.
# Offers options to remove permissions, delete services, and disable APIs,
# simplifying the process of dismantling project components after usage.
# --------------------------------------------------------------------------

# set login
./scripts/gcp_login.sh

# Set environment variables using the .env file
env_file=".env"
source $env_file


RemovePermissions() {
    # Set permissions
    PROJECT_NUMBER=`gcloud projects describe $PROJECT --format='value(projectNumber)'`

    # To execute workflow from Cloud Build
    gcloud projects remove-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/workflows.admin \
        --condition=None

    # To execute bigquery queries from Cloud Build
    gcloud projects remove-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/bigquery.admin \
        --condition=None

    # To deploy Cloud Run services from Cloud Build
    gcloud projects remove-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/run.admin \
        --condition=None
    gcloud projects remove-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/run.serviceAgent \
        --condition=None

    # To deploy Cloud Function from Cloud Build
    gcloud projects remove-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/cloudfunctions.admin \
        --condition=None
}

DeleteServices() {
    # Bigquery (Dataset)
    bq rm -r -f $DATASET

    # Cloud Function
    gcloud functions delete $FUNCTION_NAME --quiet

    # Cloud Run
    gcloud run services delete $IMAGE_NAME --region $REGION --quiet

    # Artifact Registry (Repository)
    gcloud artifacts repositories delete $IMAGE_NAME --location $REGION --quiet

    # Workflows
    gcloud workflows delete $WORKFLOW_NAME --quiet

    # Cloud Build (Trigger)
    gcloud builds triggers delete $TRIGGER_NAME

    # Storage (All Buckets)
    gsutil rm -r -f $(gsutil ls)

    # Pub/Sub (Topic, Subscription)
    gcloud pubsub topics delete $TOPIC_NAME
    gcloud pubsub subscriptions delete $SUBSCRIPTION_NAME
    gcloud pubsub subscriptions delete $SUBSCRIPTION_NAME-test
}

DisableAPIs() {
    gcloud services disable dataflow.googleapis.com
    gcloud services disable datapipelines.googleapis.com
    gcloud services disable cloudscheduler.googleapis.com
    gcloud services disable run.googleapis.com
    gcloud services disable cloudfunctions.googleapis.com
}

RemovePermissions
DeleteServices
DisableAPIs

echo "-------------------------"
echo "|   Cleanup completed   |"
echo "-------------------------"
