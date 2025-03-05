FROM python:3.12.9-slim-bookworm as copied_files

COPY serving/translate-batch/requirements.txt /srv/
COPY serving/translate-batch/*.py /srv/
COPY serving/translate-batch/docker/entry-point.sh /srv/

FROM nmt-models as models

FROM python:3.12.9-slim-bookworm

RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc git -y
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY --from=copied_files /srv/ /srv/
COPY --from=models /srv/models /srv/models

WORKDIR /srv
COPY use-models-tools/ /use-models-tools/
RUN pip3 install -r requirements.txt
RUN rm -r -f use-models-tools/

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash
