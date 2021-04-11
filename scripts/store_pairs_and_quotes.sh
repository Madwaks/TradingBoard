#!/usr/bin/env bash

set -e

docker-compose -f docker/docker-compose.services.yml down -v && docker-compose -f docker/docker-compose.services.yml up -d

sleep 5

python src/manage.py makemigrations

python src/manage.py migrate

python src/manage.py storepairs

python src/manage.py storepairquotes
