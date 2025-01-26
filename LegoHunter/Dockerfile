FROM python:latest

WORKDIR /app/

COPY app /app/app
COPY config.py /app/config.py
COPY legohunter.py /app/legohunter.py

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
