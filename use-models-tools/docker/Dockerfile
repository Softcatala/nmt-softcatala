#FROM nmt-models as models
#FROM python:3.11.0-slim-bullseye


FROM nvidia/cuda:12.3.1-base-ubuntu22.04
RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc vim -y
RUN apt-get install python3-pip python3-dev -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools
RUN apt-get install libcudnn8=8.8.1.3-1+cuda11.8 -y
RUN apt-get install cuda-toolkit-11-7 -y
COPY use-models-tools/*.mp3 /srv/flores/
COPY use-models-tools/requirements.txt /srv/
COPY use-models-tools/docker/entry-point.sh /srv/
COPY use-models-tools/setup.py /srv/
COPY use-models-tools/nmt_sc/ /srv/nmt_sc/
WORKDIR /srv
RUN pip3 install .

#COPY --from=models /srv/models /srv/models

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash
