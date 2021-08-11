FROM python:3.8.6-slim-buster as copied_files

COPY serving/translate-batch/requirements.txt /srv/
COPY serving/translate-batch/*.py /srv/
COPY serving/translate-batch/segment.srx /srv/
COPY serving/translate-batch/docker/entry-point.sh /srv/

FROM nmt-models as models

FROM python:3.8.6-slim-buster

RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY --from=copied_files /srv/ /srv/
COPY --from=models /srv/models /srv/models

WORKDIR /srv
RUN pip3 install -r requirements.txt

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash
