FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY *.py ./
COPY *.json ./

RUN apt-get update
RUN apt-get install -y cron
#RUN echo "0 */12 * * * /usr/local/bin/python3 /app/manage.py >> /var/log/cron.log 2>&1" >> /var/spool/cron/crontabs/crontab
RUN echo "* * * * * /usr/local/bin/python3 /app/manage.py >> /var/log/cron.log 2>&1" >> /var/spool/cron/crontabs/crontab
RUN crontab /var/spool/cron/crontabs/crontab
