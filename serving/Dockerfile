FROM python:3.7.6-slim-buster
RUN apt-get update && apt-get -y upgrade && apt-get install vim -y
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

ENV PORT 8700

RUN mkdir -p /srv

COPY *.py /srv/
COPY requirements.txt /srv/

WORKDIR /srv
RUN pip install -r requirements.txt


EXPOSE $PORT
#ENTRYPOINT gunicorn translate-service:app -b 0.0.0.0:$PORT
#ENTRYPOINT gunicorn translate-service:app -b 0.0.0.0:8700
ENTRYPOINT bash
