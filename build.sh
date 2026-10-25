#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Installer les dépendances Python
pip install -r requirements.txt

# 2. Collecter les fichiers statiques (CSS, JS)
python manage.py collectstatic --no-input

# 3. Appliquer les migrations de la base de données
python manage.py migrate

# 4. Charger automatiquement le Cameroun si la base est neuve
python manage.py charger_cameroun