# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV RUNTIME_DEPENDENCIES="ffmpeg"

RUN apt-get update \
    && apt-get install -y ${RUNTIME_DEPENDENCIES} \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
EXPOSE 8080
EXPOSE 5000


CMD python3 main.py