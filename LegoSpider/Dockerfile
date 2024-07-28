FROM python:latest

WORKDIR /app

COPY . /app/
RUN pip3 install -r requirements.txt

RUN apt-get update
RUN apt-get install -y cron
