#!/bin/bash -eu
# Workspaceでcatkin_makeを実行する
TAG_NAME=${1:-""}
[ "${TAG_NAME}" = "" ] || TAG_NAME=:${TAG_NAME}
HOST_WS=${2:-"$HOME/catkin_ws"}
CONTAINER_WS=/home/developer/catkin_ws

docker exec
    ${DEV_DOCKER_IMAGE_NAME} \
    bash -c "cd ${CONTAINER_WS} && catkin_make"
