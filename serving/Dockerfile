FROM python:3.7.6-slim-buster as generate_data

RUN mkdir -p /models/eng-cat
COPY models/eng-cat/ models/eng-cat/
COPY models/eng-cat/1/assets/*.model  /srv/
COPY models/eng-cat/1/assets/model_description.txt  /srv/model_description.txt
COPY serving/*.py /srv/
COPY serving/requirements.txt /srv/
COPY serving/docker/entry-point.sh /srv/

FROM opennmt/tensorflow-serving:2.1.0

#RUN mkdir -p /srv
COPY --from=generate_data /srv/ /srv/
COPY --from=generate_data /models/ /models/
RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

EXPOSE 8700

WORKDIR /srv
RUN pip3 install -r requirements.txt

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash


