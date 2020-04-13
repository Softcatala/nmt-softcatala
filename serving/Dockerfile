FROM python:3.7.6-slim-buster as generate_data

RUN mkdir -p /models/eng-cat
COPY models/eng-cat/ models/eng-cat/
COPY models/eng-cat/1/assets/*.model  /srv/
COPY models/eng-cat/1/assets/model_description.txt  /srv/model-description-engcat.txt

COPY models/cat-eng/ models/cat-eng/	
COPY models/cat-eng/1/assets/model_description.txt  /srv/model-description-cateng.txt
COPY serving/*.py /srv/
COPY serving/models.conf /srv/models.conf
COPY serving/requirements.txt /srv/
COPY serving/docker/entry-point.sh /srv/
#COPY serving/tf-optimised/tensorflow-2.1.0-cp27-cp27mu-linux_x86_64.whl /srv/


FROM opennmt/tensorflow-serving:2.1.0

COPY --from=generate_data /srv/ /srv/
COPY --from=generate_data /models/ /models/
RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

EXPOSE 8700

WORKDIR /srv
RUN pip3 install -r requirements.txt
#RUN pip3 install --ignore-installed --upgrade tensorflow-2.1.0-cp27-cp27mu-linux_x86_64.whl

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash


