#!/bin/bash

# Get a list of all stopped container IDs
stopped_containers=$(docker ps -aq --filter "status=exited")

# Loop through the stopped container IDs
for container_id in $stopped_containers; do
  # Get the image ID associated with the stopped container
  image_id=$(docker inspect -f '{{.Image}}' $container_id)

  # Get a list of volumes associated with the container
  volumes=$(docker inspect -f '{{range .Mounts}}{{.Name}} {{end}}' $container_id)

  # Remove the stopped container
  docker rm $container_id
  echo "Deleted container $container_id"

  # Remove the associated image
  docker rmi $image_id
  echo "Deleted image $image_id"

  # Remove the associated volumes
  for volume in $volumes; do
    if [ -n "$volume" ]; then
      docker volume rm $volume
      echo "Deleted volume $volume"
    fi
  done
done

##!/bin/bash
#
## Get a list of all image IDs
#all_images=$(docker images -q)
#
## Get a list of all container IDs
#all_containers=$(docker ps -aq)
#
## Loop through the image IDs
#for image_id in $all_images; do
#  # Check if the image is in use by any containers
#  if [[ ! $all_containers =~ $image_id ]]; then
#    # If not in use, delete the image
#    docker rmi $image_id
#    echo "Deleted image $image_id"
#  fi
#done

