#!/bin/bash

python manage.py makemigrations
python manage.py migrate
mkdir media
exec gunicorn run_text_project.wsgi:application --workers=$GUNICORN_WORKERS --bind "$GUNICORN_IP":"$GUNICORN_PORT"

