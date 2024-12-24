FROM python:latest

WORKDIR /app/

COPY app /app/app
COPY config.py /app/config.py
COPY legohunter.py /app/legohunter.py
COPY config.json /app/config.json

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
