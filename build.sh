#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Crée votre compte administrateur en ligne de manière automatique
python manage.py createsuperuser --no-input || true