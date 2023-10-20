#!/bin/bash

# Remove stopped containers and their associated images and volumes
stopped_containers=$(docker ps -aq --filter "status=exited")
for container_id in $stopped_containers; do
  image_id=$(docker inspect -f '{{.Image}}' $container_id)
  volumes=$(docker inspect -f '{{range .Mounts}}{{.Name}} {{end}}' $container_id)
  docker rm $container_id
  echo "Deleted container $container_id"
  docker rmi $image_id
  echo "Deleted image $image_id"
  for volume in $volumes; do
    if [ -n "$volume" ]; then
      docker volume rm $volume
      echo "Deleted volume $volume"
    fi
  done
done

# Remove images not related to any container
unused_images=$(docker images -q --filter "dangling=true")
for image_id in $unused_images; do
  docker rmi $image_id
  echo "Deleted unused image $image_id"
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

