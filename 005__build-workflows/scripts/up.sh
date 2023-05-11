#!/bin/bash

# set login
./scripts/set_gcp_login.sh

# Load environment variables
env_file=".env"
source $env_file

# Set permissions
gcloud projects add-iam-policy-binding $PROJECT --member=user:$ACCOUNT --role=roles/workflows.editor
