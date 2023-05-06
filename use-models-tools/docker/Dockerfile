FROM nmt-models as models
FROM python:3.11.0-slim-bullseye

RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc vim -y
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY use-models-tools/requirements.txt /srv/
COPY use-models-tools/docker/entry-point.sh /srv/
COPY use-models-tools/setup.py /srv/
COPY use-models-tools/nmt_sc/ /srv/nmt_sc/
WORKDIR /srv
RUN pip3 install .

COPY --from=models /srv/models /srv/models

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash
