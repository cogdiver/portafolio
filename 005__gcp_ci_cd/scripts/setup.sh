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

# Path to the .env file
env_file=".env"

# Source the .env file to load any existing variables
source $env_file


Help() {
    # Display options menu
    echo "usage: ./setup.sh [options]"
    echo
    echo "-h | --help          Print this message"
    echo "-a | --apis          Enable Required APIs"
    echo "-c | --create        Create Project services"
    echo "-p | --permissions   Add Project Permissions"
}

EnableAPIs() {
    gcloud services enable dataflow.googleapis.com
    gcloud services enable datapipelines.googleapis.com
    gcloud services enable cloudscheduler.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable cloudfunctions.googleapis.com
}

CreateServices() {
    # Cloud Buil (Trigger)
    gcloud builds triggers create github \
        --name=$TRIGGER_NAME \
        --repo-name=$GITHUB_REPO_NAME \
        --repo-owner=$GITHUB_REPO_OWNER \
        --branch-pattern=$BRANCH_PATTERN \
        --build-config=$FOLDER/cloudbuild.yaml \
        --substitutions=_FOLDER="$FOLDER",_WORKFLOW_NAME="$WORKFLOW_NAME",_BUCKET_NAME="$BUCKET_NAME",_PROJECT="$PROJECT",_IMAGE_NAME="$IMAGE_NAME",_REGION="$REGION",_FUNCTION_NAME="$FUNCTION_NAME",_DATASET="$DATASET"

    # Storage (Bucket)
    gsutil mb gs://$BUCKET_NAME

    # Bigquery (Dataset)
    bq mk $DATASET

    # Artifact Registry (Repository)
    gcloud artifacts repositories create $IMAGE_NAME \
        --repository-format=docker \
        --location=$REGION

    # Pub/Sub (Topic, Subscription)
    gcloud pubsub topics create $TOPIC_NAME
    gcloud pubsub subscriptions create $SUBSCRIPTION_NAME --topic $TOPIC_NAME
    gcloud pubsub subscriptions create $SUBSCRIPTION_NAME-test --topic $TOPIC_NAME

    # # Dataflow (Template)
    # gcloud dataflow jobs run $JOB_NAME \
    #     --gcs-location gs://dataflow-templates-$REGION/latest/PubSub_Subscription_to_BigQuery \
    #     --region $REGION \
    #     --staging-location gs://$BUCKET_NAME/temp \
    #     --parameters inputSubscription=projects/$PROJECT/subscriptions/$SUBSCRIPTION_NAME,outputTableSpec=$PROJECT:$DATASET.$OUTPUT_TABLE

}

AddtPermissions() {
    # Set permissions
    PROJECT_NUMBER=`gcloud projects describe $PROJECT --format='value(projectNumber)'`

    # To execute workflow from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/workflows.admin \
        --condition=None

    # To execute bigquery queries from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/bigquery.admin \
        --condition=None

    # To deploy Cloud Run services from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/run.admin \
        --condition=None
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/run.serviceAgent \
        --condition=None

    # To deploy Cloud Function from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/cloudfunctions.admin \
        --condition=None

    # To write pub/sub message on bigquery
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com \
        --role=roles/bigquery.admin \
        --condition=None
}


# Options
if [[ $# == 0 ]]; then
    Help
elif [[ $# == 1 ]]; then
    case "$1" in
        -h | --help) Help;;
        -a | --apis) EnableAPIs;;
        -c | --create) CreateServices;;
        -p | --permissions) AddtPermissions;;
        *) echo "'$1' is not a valid option. See ./setup.sh --help"
        Help;;
    esac
else
    echo "Only one option is allowed. See ./setup.sh --help"
fi
