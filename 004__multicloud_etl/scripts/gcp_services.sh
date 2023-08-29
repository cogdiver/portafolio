#!/bin/bash

# set login
./scripts/gcp_login.sh

# enable apis
gcloud services disable composer.googleapis.com --force
gcloud services enable composer.googleapis.com

# create buckets
gsutil mb -l us-east1 gs://<BUCKET_1>
gsutil mb -l us-east1 gs://<BUCKET_3>

# create dataset
bq mk <DATASET>

# Create store procedures
# cat bigquery.sql | bq query --nouse_legacy_sql
