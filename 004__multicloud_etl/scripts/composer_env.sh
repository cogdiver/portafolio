#!/bin/bash

# set login
./scripts/gcp_login.sh

# create composer enviroment
gcloud composer environments create <ENVIRONMENT_NAME> \
  --location <LOCATION>

COMPOSER_DAGS=`gcloud composer environments describe <ENVIRONMENT_NAME> \
  --location <LOCATION> \
  --format='value(config.dagGcsPrefix)'`

COMPOSER_URL=`gcloud composer environments describe <ENVIRONMENT_NAME> \
  --location <LOCATION> \
  --format='value(config.airflowUri)'`

echo COMPOSER_DAGS = $COMPOSER_DAGS
echo COMPOSER_URL = $COMPOSER_URL
