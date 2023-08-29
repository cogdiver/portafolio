#!/bin/bash

# ------------------------------------------------------------------------------
# This script is designed to replace placeholders in files with provided values.
# It reads environment variables from the .env file and uses them to replace
# placeholders files located in the project.
# ------------------------------------------------------------------------------

# Load environment variables from .env file
env_file=".env"
source $env_file

# # Replace the '<PROJECT>' placeholder into bigquery/*.sql files
# sed -i 's/<PROJECT>/'$PROJECT'/g' bigquery/*.sql

echo "Placeholder replacement completed."
