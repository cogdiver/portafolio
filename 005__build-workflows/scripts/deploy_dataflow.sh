#!/bin/bash

# set login
# ./scripts/set_gcp_login.sh

# Load environment variables
env_file=".env"
source $env_file


# python3 template/template_count.py \
#   --runner=DataflowRunner \
#   --project=$PROJECT \
#   --region=$REGION \
#   --temp_location=gs://005__build-workflows/temp/ \
#   # --staging_location=<STAGING_LOCATION>

# gsutil cp template/*  gs://005__build-workflows/template/
# gcloud dataflow jobs run 005__build_workflows \
#   --gcs-location gs://$BUCKET_NAME/template/template_count.py \
#   --region $REGION
# --parameters='1,2'
# --parameters inputFile=gs://$BUCKET_NAME/template/input.txt,output=gs://$BUCKET_NAME/output

# gcloud dataflow jobs run 005__build_workflows \
#   --gcs-location gs://dataflow-templates/latest/Word_Count \
#   --region $REGION \
#   --parameters inputFile=gs://$BUCKET_NAME/template/input.txt,output=gs://$BUCKET_NAME/template/output.txt
# gsutil cp gs://005__build-workflows/template/output.txt template/


gcloud dataflow flex-template run build-workflows \
  --template-file-gcs-location gs://$BUCKET_NAME/template/template_count.py \
  --temp-location gs://$BUCKET_NAME/temp/ \
  --region $REGION \
  --parameters inputFile=gs://$BUCKET_NAME/template/input.txt,output=gs://$BUCKET_NAME/output
  # --parameters='1,2'
