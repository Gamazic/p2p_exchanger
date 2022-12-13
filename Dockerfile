FROM python:3.10.7-slim-buster

RUN apt-get update && apt-get install libpq-dev python3-dev curl -y

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .