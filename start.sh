#!/usr/bin/env bash
# Roda no Render toda vez que o site liga: prepara o banco e inicia o servidor
python manage.py migrate --noinput
python manage.py loaddata projetos_iniciais
python manage.py createsuperuser --noinput || true
exec gunicorn reassocia_site.wsgi --bind 0.0.0.0:$PORT
