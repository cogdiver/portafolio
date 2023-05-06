#!/bin/bash

# Read .env file for enviroment variables
env_file=".env"

if [[ ! -e $env_file ]]; then
  read -p "GCP account: " account
  read -p "GCP project: " project

  echo "ACCOUNT=$account
PROJECT=$project" > $env_file
fi

source $env_file

# Set GCP variables
gcloud config set account $ACCOUNT
gcloud config set project $PROJECT
