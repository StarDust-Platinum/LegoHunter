FROM python:latest

WORKDIR /app

COPY run.py /app/run.py

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

RUN apt-get update
RUN apt-get install -y cron
