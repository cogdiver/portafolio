#!/bin/bash

# set login
./scripts/set_gcp_login.sh

# Load environment variables
env_file=".env"
source $env_file

# Create Service Account
gcloud iam service-accounts create $SERVICE_ACCOUNT


# # Set permissions
gcloud projects add-iam-policy-binding $PROJECT --member=serviceAccount:$SERVICE_ACCOUNT@$PROJECT.iam.gserviceaccount.com --role=roles/workflows.admin
# gcloud builds triggers describe $TRIGGER_NAME --format="value(substitutions._CLOUD_BUILD_SERVICE_ACCOUNT)"
