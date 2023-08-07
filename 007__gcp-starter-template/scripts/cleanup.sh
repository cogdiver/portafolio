#!/bin/bash

# ----------------------------------------------------------------------------------
# This script is designed to clean up the Docker environment. It stops and removes
# all containers, networks, and volumes associated with the docker-compose.yml file,
# and also deletes any images built by docker-compose. It's meant to be used in a
# development environment to reset the state and free up resources.
# ----------------------------------------------------------------------------------

# Stop and remove all containers, networks and volumes
# defined in docker-compose.yml, and remove images
docker-compose down --volumes --rmi all

echo "Environment cleaned successfully."
