#!/bin/bash -xe

eval $(aws ecr get-login)
docker tag wichita-ecr-andy-docker-app:latest 052763798005.dkr.ecr.us-east-1.amazonaws.com/wichita-ecr-andy-docker-app:v${CIRCLE_BUILD_NUM}

docker push 052763798005.dkr.ecr.us-east-1.amazonaws.com/wichita-ecr-andy-docker-app:v${CIRCLE_BUILD_NUM}

./deployer.py v${CIRCLE_BUILD_NUM}
