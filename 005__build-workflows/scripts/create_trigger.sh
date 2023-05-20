#!/bin/bash

# set login
./scripts/set_gcp_login.sh

# Load environment variables
env_file=".env"
source $env_file

# Create trigger for github repository
# gcloud builds triggers delete $TRIGGER_NAME
gcloud builds triggers create github \
  --name=$TRIGGER_NAME \
  --repo-name=$GITHUB_REPO_NAME \
  --repo-owner=$GITHUB_REPO_OWNER \
  --branch-pattern=$BRANCH_PATTERN \
  --build-config=$BUILD_CONFIG_FILE
