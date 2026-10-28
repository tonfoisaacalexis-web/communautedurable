#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# 1. Crée le compte administrateur en ligne de manière automatique
python manage.py createsuperuser --no-input || true

# 2. Charge les 58 départements de manière 100% compatible
python manage.py charger_cameroun