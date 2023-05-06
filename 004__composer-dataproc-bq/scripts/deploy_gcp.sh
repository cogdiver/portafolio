#!/bin/bash

# set login
./scripts/set_gcp_login.sh

# deploy dags
gsutil cp dags/*.py gs://<COMPOSER_DAGS>/
