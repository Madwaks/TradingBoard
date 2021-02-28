#!/usr/bin/env bash

docker-compose -f docker/docker-compose.services.yml down -v
docker-compose -f docker/docker-compose.services.yml up -d
sleep 2
python src/manage.py migrate
python src/manage.py ${@}
