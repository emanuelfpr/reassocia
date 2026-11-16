#!/usr/bin/env bash
# Roda no Render a cada deploy: instala e prepara os arquivos estáticos
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
