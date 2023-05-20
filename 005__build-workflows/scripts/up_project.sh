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
    echo "-p | --permissions   Set Project Permissions"
}

CreateServices() {
    # Storage (Bucket)
    gsutil mb gs://$BUCKET_NAME

    # Bigquery (Dataset)
    bq mk $DATASET
}

SetPermissions() {
    # Set permissions
    PROJECT_NUMBER=`gcloud projects describe $PROJECT --format='value(projectNumber)'`

    # To execute workflow from cloudbuild
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/workflows.admin

    # To execute bigquery queries from cloudbuild
    gcloud projects add-iam-policy-binding $PROJECT \
        --member=serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com \
        --role=roles/bigquery.jobUser
}


# 
if [[ $# == 0 ]]; then
    Help
elif [[ $# == 1 ]]; then
    case "$1" in
        -h | --help) Help;;
        -c | --create) CreateServices;;
        -p | --permissions) SetPermissions;;
        *) echo "'$1' is not a valid option. See ./up_project.sh --help"
        Help;;
    esac
else
    echo "Only one option is allowed. See ./up_project.sh --help"
fi


