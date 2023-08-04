#!/bin/bash
# Script to build ETL service

# Build services
echo "+---------------------------------+"
echo "|      Building services....      |"
echo "+---------------------------------+"

docker-compose up airflow-init -d
docker-compose up -d
