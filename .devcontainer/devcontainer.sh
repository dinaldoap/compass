#!/bin/bash

DEVCONTAINER=$(docker ps --all | grep 'vsc-compass' | awk '{print $1}')
docker stop "${DEVCONTAINER}"
docker rm "${DEVCONTAINER}"
docker volume rm 'compass_vscode-server'
docker build --file=.devcontainer/devcontainer.dockerfile .
exit 0