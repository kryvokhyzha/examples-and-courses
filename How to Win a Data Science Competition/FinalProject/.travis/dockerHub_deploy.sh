#!/bin/sh

if [ "$TRAVIS_BRANCH" = "master" ] && [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
    TAG="latest"
    
    docker login -u $DOCKER_USER -p $DOCKER_PASS
    docker-compose build --pull
    docker-compose push
    docker logout
else
    TAG="$TRAVIS_BRANCH"
fi
