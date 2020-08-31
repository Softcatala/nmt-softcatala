FROM python:3.8.2-slim-buster

RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY use-models-tools/requirements.txt /srv/
WORKDIR /srv
RUN pip3 install -r requirements.txt

COPY use-models-tools/*.py /srv/
COPY use-models-tools/segment.srx /srv/
COPY use-models-tools/docker/entry-point.sh /srv/

COPY models/eng-cat/ctranslate2/ /srv/models/eng-cat/
COPY models/cat-eng/ctranslate2/ /srv/models/cat-eng/
COPY models/eng-cat/exported/assets/*.model /srv/models/tokenizer/

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash
