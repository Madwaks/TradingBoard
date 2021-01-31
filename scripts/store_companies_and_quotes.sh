#!/usr/bin/env bash

set -e

python src/manage.py makemigrations

python src/manage.py migrate

python src/manage.py storecompanies

python src/manage.py downloadquotes

python src/manage.py storequotes
