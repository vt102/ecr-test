#!/bin/bash -xe

eval $(aws ecr get-login)
docker tag wichita-ecr-andy-docker-app:latest 052763798005.dkr.ecr.us-east-1.amazonaws.com/wichita-ecr-andy-docker-app:latest
docker push 052763798005.dkr.ecr.us-east-1.amazonaws.com/wichita-ecr-andy-docker-app:latest
docker tag wichita-ecr-andy-docker-app:latest 052763798005.dkr.ecr.us-east-1.amazonaws.com/wichita-ecr-andy-docker-app:${CIRCLE_SHA1}
docker push 052763798005.dkr.ecr.us-east-1.amazonaws.com/wichita-ecr-andy-docker-app:${CIRCLE_SHA1}
