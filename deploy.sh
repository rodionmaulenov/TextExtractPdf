#!/bin/bash
set -e

# Navigate to the project directory
cd /home/rodion/TEXT_EXTRACT_PDF

# Source environment variables
source .env

# Log in to GitHub Packages
docker login ghcr.io -u $NAMESPACE -p $PERSONAL_ACCESS_TOKEN

# Pull Docker images
docker pull $APP_IMAGE
docker pull $NGINX_IMAGE
docker pull $ACME_IMAGE

# Bring up containers using Docker Compose
docker-compose -f docker-compose.prod.yml up -d