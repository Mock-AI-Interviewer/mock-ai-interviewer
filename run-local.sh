#!/bin/bash
set -a &&
source ./backend/.env &&
source ./frontend/.env &&
set +a &&
docker-compose -f docker-compose.local.yml build &&
docker-compose -f docker-compose.local.yml up -d
