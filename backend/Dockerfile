FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY cronjobs /etc/cron.d/cronjobs
RUN chmod 0644 /etc/cron.d/cronjobs
RUN touch /var/log/cron.log

# RUN /usr/bin/crontab /etc/cron.d/cronjobs

COPY entrypoint.sh . 
RUN chmod +x /app/entrypoint.sh


RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
