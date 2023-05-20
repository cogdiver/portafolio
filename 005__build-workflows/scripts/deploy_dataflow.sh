#!/bin/bash

# set login
./scripts/set_gcp_login.sh

# Load environment variables
env_file=".env"
source $env_file


python dataflow_pipeline.py \
  --runner=DataflowRunner \
  --project=$PROJECT \
  --region=$REGION \
  --temp_location=<TEMP_LOCATION> \
  --staging_location=<STAGING_LOCATION>

gcloud dataflow jobs run 005_build_worflows \
  --gcs-location gs://$BUCKET_NAME/template/template_count.py \
  --region $REGION \
  --parameters inputFile=gs://$BUCKET_NAME/input.txt,output=gs://$BUCKET_NAME/output
