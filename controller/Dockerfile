FROM python:3.8.0-slim-buster

ARG PORT_WEB_API
ARG PORT_UDP_SERVER

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE $PORT_WEB_API
EXPOSE $PORT_UDP_SERVER