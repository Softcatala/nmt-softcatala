FROM python:3.7.6-slim-buster

COPY serving/translate-service/*.py /srv/
COPY serving/translate-service/requirements.txt /srv/
COPY serving/translate-service/docker/entry-point.sh /srv/
RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

EXPOSE 8700

WORKDIR /srv
RUN pip3 install -r requirements.txt

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash