#!/bin/bash

# Get a list of all image IDs
all_images=$(docker images -q)

# Get a list of all container IDs
all_containers=$(docker ps -aq)

# Loop through the image IDs
for image_id in $all_images; do
  # Check if the image is in use by any containers
  if [[ ! $all_containers =~ $image_id ]]; then
    # If not in use, delete the image
    docker rmi $image_id
    echo "Deleted image $image_id"
  fi
done
