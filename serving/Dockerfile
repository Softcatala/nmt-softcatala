FROM python:3.7.6-slim-buster
RUN apt-get update && apt-get -y upgrade

ENV PORT 8700

RUN mkdir -p /srv

COPY Pipfile /srv/
COPY *.py /srv/

WORKDIR /srv

RUN pip install pipenv
RUN pipenv install

EXPOSE $PORT
ENTRYPOINT pipenv run gunicorn translate-service:app -b 0.0.0.0:$PORT
