#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the variable for the Docker Compose file
DOCKER_COMPOSE_FILE="docker-compose.local.yml"

source ./scripts/setup-env.sh
source ./scripts/get-service-selection.sh
SELECTED_SERVICES=$(get_service_selection)
docker-compose -f $DOCKER_COMPOSE_FILE down
docker-compose -f $DOCKER_COMPOSE_FILE build $SELECTED_SERVICES
docker-compose -f $DOCKER_COMPOSE_FILE up -d $SELECTED_SERVICES
