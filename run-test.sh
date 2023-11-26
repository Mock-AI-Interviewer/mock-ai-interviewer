#!/bin/bash
set -a &&
source ./backend/.env &&
source ./frontend/.env &&
set +a &&
docker-compose -f docker-compose.yml up --build