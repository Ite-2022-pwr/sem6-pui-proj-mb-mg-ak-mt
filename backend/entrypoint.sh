#!/bin/bash
cron
/usr/bin/crontab /etc/cron.d/cronjobs
python manage.py runserver 0.0.0.0:8000