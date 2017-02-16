#!/bin/bash

set -e

export DOCKER_IP=192.168.99.100

[[ -n $TRAVIS ]] || docker-compose build
[[ -n $TRAVIS ]] || docker-compose pull
[[ -n $TRAVIS ]] || docker-compose up -d

set +e
behave "$@"
RET=$?
[[ -n $TRAVIS ]] || docker-compose stop
[[ -n $TRAVIS ]] || docker-compose rm --force

exit ${RET}
