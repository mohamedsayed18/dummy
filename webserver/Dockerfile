FROM python:3.8.0-slim-buster

ARG PORT_HTTP_SERVER

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE $PORT_HTTP_SERVER
