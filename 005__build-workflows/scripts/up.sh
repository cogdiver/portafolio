#!/bin/bash

# set login
./scripts/set_gcp_login.sh

# Load environment variables
env_file=".env"
source $env_file

# Create Service Account
# gcloud iam service-accounts create $SERVICE_ACCOUNT

# Set permissions
project_number=`gcloud projects describe $PROJECT --format='value(projectNumber)'`
gcloud projects add-iam-policy-binding $PROJECT --member=serviceAccount:$project_number@cloudbuild.gserviceaccount.com --role=roles/workflows.admin

