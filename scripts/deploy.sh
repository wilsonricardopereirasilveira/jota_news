#!/bin/bash
# Simple deployment script
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn jota_news.wsgi:application
