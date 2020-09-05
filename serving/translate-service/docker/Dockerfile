FROM python:3.8.2-slim-buster

RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY serving/translate-service/requirements.txt /srv/
WORKDIR /srv
RUN pip3 install -r requirements.txt

COPY serving/translate-service/*.py /srv/
COPY serving/translate-service/segment.srx /srv/
COPY serving/translate-service/docker/entry-point.sh /srv/

COPY models/eng-cat/ctranslate2/ /srv/models/eng-cat/
COPY models/cat-eng/ctranslate2/ /srv/models/cat-eng/
COPY models/eng-cat/tokenizer/*.model /srv/models/tokenizer/


EXPOSE 8700


ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash
