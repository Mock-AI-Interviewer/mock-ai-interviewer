#!/bin/bash

# Function to get selected services from user
get_service_selection() {
    echo "Enter the service names separated by space (e.g., frontend backend):" >&2
    read -ra SERVICES # Read services into an array
    echo "${SERVICES[@]}" # Output the selected services
}