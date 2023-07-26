#!/bin/bash
echo "Waiting..."
sleep 5
python manage.py migrate --no-input
python manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=$A_PASSWORD python manage.py createsuperuser --username $A_NAME --email $A_EMAIL --noinput

gunicorn project_blog.wsgi:application --bind 0.0.0.0:8015
