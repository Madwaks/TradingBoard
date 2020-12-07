#!/usr/bin/env bash

APPS=$(python /app/manage.py shell -c 'from django.conf import settings; print(settings.LOCAL_APPS)' | tr -d '[],')

echo "$APPS"
echo "Running migrations"
python /app/manage.py makemigrations #"${APPS}"

echo "Running migrate"
python /app/manage.py migrate

echo "Running server"
python /app/manage.py runserver 0.0.0.0:8000