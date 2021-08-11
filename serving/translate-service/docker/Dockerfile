FROM python:3.8.6-slim-buster as copied_files

COPY serving/translate-service/*.py /srv/
COPY serving/translate-service/segment.srx /srv/
COPY serving/translate-service/docker/entry-point.sh /srv/
COPY serving/translate-service/gender-bias-terms.txt /srv/

FROM nmt-models as models

FROM python:3.8.6-slim-buster

RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY serving/translate-service/requirements.txt /srv/
WORKDIR /srv
RUN pip3 install -r requirements.txt

COPY --from=copied_files /srv/ /srv/
COPY --from=models /srv/models /srv/models

EXPOSE 8700

ENTRYPOINT /srv/entry-point.sh

