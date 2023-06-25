#!/bin/bash

# set login
./scripts/set_gcp_login.sh

# Load environment variables
env_file=".env"
source $env_file


# Functions
Help() {
    # Display options menu
    echo "usage: ./up_project.sh [options]"
    echo
    echo "-h | --help          Print this message"
    echo "-p | --permissions   Remove Project Permissions"
    echo "-d | --delete        Delete Project services"
    echo "-a | --apis          Disable APIs"
}

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


# Options
if [[ $# == 0 ]]; then
    Help
elif [[ $# == 1 ]]; then
    case "$1" in
        -h | --help) Help;;
        -p | --permissions) RemovePermissions;;
        -d | --delete) DeleteServices;;
        -a | --apis) DisableAPIs;;
        *) echo "'$1' is not a valid option. See ./up_project.sh --help"
        Help;;
    esac
else
    echo "Only one option is allowed. See ./up_project.sh --help"
fi
