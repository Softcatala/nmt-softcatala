FROM opennmt/tensorflow-serving:2.1.0 

RUN mkdir -p /models/eng-cat
COPY models/eng-cat/ models/eng-cat/

RUN apt-get update && apt-get -y upgrade 
RUN apt-get install vim -y
RUN apt-get install python3-pip -y
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

ENV PORT 8700
EXPOSE $PORT

RUN mkdir -p /srv

COPY models/eng-cat/1/assets/*.model  /srv/
COPY serving/*.py /srv/
COPY serving/requirements.txt /srv/
COPY serving/docker/entry-point.sh /srv/

WORKDIR /srv
RUN pip3 install -r requirements.txt

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash


