#!/bin/bash

# ----------------------------------------------------------------------------
# This script builds a Docker image and then runs a container based on that
# image, initiating the creation of a template with Cookiecutter.
#
# - The build command creates an image named "$CONTAINER_NAME" from the
#   Dockerfile in the current directory.
# - The run command starts a container based on the "$CONTAINER_NAME" image,
#   attaching the terminal to the container's standard input and output, thus
#   allowing the user to interact with Cookiecutter to create the template.
# - The start command resumes the container if it was stopped.
# - The copy command copies files from the container's "/service/temp/"
#   directory to the current directory on the host.
# - The stop command gracefully stops the running container.
# - The remove command deletes the container.
# ----------------------------------------------------------------------------

CONTAINER_NAME="temporary_container_template"

# Build the Docker image
# -t $CONTAINER_NAME: Name the image "$CONTAINER_NAME"
# . : Build context is the current directory (containing the Dockerfile)
docker build -t $CONTAINER_NAME .

# Run a container based on the built image
# -it: Keep STDIN open and allocate a pseudo-TTY, allowing interaction with Cookiecutter
# $CONTAINER_NAME: Name of the image to run
docker run -it --name $CONTAINER_NAME $CONTAINER_NAME

# Start the container if it was stopped
docker start $CONTAINER_NAME

# Copy files from the container's "/service/temp/" directory to the current directory on the host
docker cp -a $CONTAINER_NAME:/service/temp/. .

# Gracefully stop the running container
docker stop $CONTAINER_NAME

# Delete the container
docker rm $CONTAINER_NAME
