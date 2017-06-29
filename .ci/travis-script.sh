#!/bin/bash

set -e -x

docker build -t dainco/readability ./js/readability
docker build -t dainco/article-extractor./python

if [[ "${TRAVIS_BRANCH}" == "master" ]]; then
  docker login -u="${DOCKER_USERNAME}" -p="${DOCKER_PASSWORD}";
  docker push dainco/readability
  docker push dainco/article-extractor
fi
