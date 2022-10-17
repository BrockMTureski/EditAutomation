# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV RUNTIME_DEPENDENCIES="ffmpeg"
RUN apt-get update \
    &&apt-get install -y ${RUNTIME_DEPENDENCIES} \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]