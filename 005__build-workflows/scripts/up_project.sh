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
    echo "-c | --create        Create Project services"
    echo "-a | --apis          Enable Required APIs"
    echo "-p | --permissions   Set Project Permissions"
}

CreateServices() {
    # Cloud Buil (Trigger)
    gcloud builds triggers create github \
        --name=$TRIGGER_NAME \
        --repo-name=$GITHUB_REPO_NAME \
        --repo-owner=$GITHUB_REPO_OWNER \
        --branch-pattern=$BRANCH_PATTERN \
        --build-config=$BUILD_CONFIG_FILE

    # Storage (Bucket)
    gsutil mb gs://$BUCKET_NAME

    # Bigquery (Dataset)
    bq mk $DATASET

    # Artifact Registry (Repository)
    gcloud artifacts repositories create $IMAGE_NAME \
        --repository-format=docker \
        --location=$REGION
}

EnableAPIs() {
    gcloud services enable dataflow.googleapis.com
    gcloud services enable datapipelines.googleapis.com
    gcloud services enable cloudscheduler.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable cloudfunctions.googleapis.com
}

SetPermissions() {
    # Set permissions
    PROJECT_NUMBER=`gcloud projects describe $PROJECT --format='value(projectNumber)'`

    # To execute workflow from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/workflows.admin

    # To execute bigquery queries from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/bigquery.admin

    # To deploy Cloud Run services from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/run.admin
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/run.serviceAgent

    # To deploy Cloud Function from Cloud Build
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/cloudfunctions.admin
}

# Options
if [[ $# == 0 ]]; then
    Help
elif [[ $# == 1 ]]; then
    case "$1" in
        -h | --help) Help;;
        -c | --create) CreateServices;;
        -a | --apis) EnableAPIs;;
        -p | --permissions) SetPermissions;;
        *) echo "'$1' is not a valid option. See ./up_project.sh --help"
        Help;;
    esac
else
    echo "Only one option is allowed. See ./up_project.sh --help"
fi
