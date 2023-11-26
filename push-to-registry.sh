#!/bin/bash

# Load Env Variables
set -a &&
source ./backend/.env &&
source ./frontend/.env &&
set +a &&

# Get a list of services from docker-compose file
services=$(docker-compose -f docker-compose.local.yml config --services)
echo "Available services:"
echo "$services"

# Ask the user to choose a service
echo "Please enter the service name you want to build (e.g., frontend, backend):"
read chosen_service

# Check if the entered service is valid
if ! [[ $services =~ (^|[[:space:]])$chosen_service($|[[:space:]]) ]]; then
    echo "Error: Invalid service name."
    exit 1
fi

# List AWS profiles
echo "Available AWS profiles:"
awk '/^\[/{if (NR>1) print ""; print $0}' ~/.aws/config | sed 's/\[\|\]//g'

# Ask the user to choose an AWS profile
echo "Please enter the AWS profile you want to use:"
read aws_profile

# Set the chosen AWS profile
export AWS_PROFILE=$aws_profile

# Login to AWS ECR
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/h2s4i0x5

# Build, tag, and push the image
docker-compose -f docker-compose.local.yml build $chosen_service &&
docker tag mock-ai-interviewer-$chosen_service:latest public.ecr.aws/h2s4i0x5/mock-ai-interviewer-$chosen_service &&
docker push public.ecr.aws/h2s4i0x5/mock-ai-interviewer-$chosen_service
