#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# AJOUT : Crée le compte administrateur en ligne en lisant vos variables Render
python manage.py createsuperuser --no-input || true