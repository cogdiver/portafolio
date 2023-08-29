#!/bin/bash

Help() {
    # Display options menu
    echo "usage: ./scripts/down.sh [options]"
    echo
    echo "-h | --help     Print this message"
    echo "-l | --local    Remove Local environment"
    echo "-c | --cloud    Remove Cloud enviroment"
}

DownCloud() {
    # Delete composer enviroment
    gcloud composer environments delete <ENVIRONMENT_NAME> \
        --location <LOCATION>
}

DownLocal() {
    # Remove local containers
    docker-compose down --volumes --rmi all
}

  
if [[ $# == 0 ]]; then
    Help
elif [[ $# == 1 ]]; then
    case "$1" in
        -h | --help) Help;;
        -l | --local) DownLocal;;
        -c | --cloud) DownCloud;;
        *) echo "'$1' is not a valid option. See ./scripts/down.sh --help"
            Help;;
    esac
else
    echo "Only one option is allowed. See ./scripts/down.sh --help"
fi
