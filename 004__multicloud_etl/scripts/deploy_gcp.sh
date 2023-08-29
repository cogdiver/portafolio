#!/bin/bash

# set login
./scripts/gcp_login.sh

# deploy dags
gsutil cp dags/*.py gs://<COMPOSER_DAGS>/
