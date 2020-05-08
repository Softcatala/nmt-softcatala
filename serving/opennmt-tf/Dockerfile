FROM opennmt/tensorflow-serving:2.1.0

EXPOSE 8500
EXPOSE 8501

RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY models/eng-cat/ models/eng-cat/
COPY models/cat-eng/ models/cat-eng/
COPY serving/opennmt-tf/models.conf /srv/models.conf
COPY serving/opennmt-tf/entry-point.sh /srv/
COPY serving/opennmt-tf/tf-optimised/tensorflow-2.1.0-cp36-cp36m-linux_x86_64.whl /srv/

WORKDIR /srv
RUN pip3 install --ignore-installed --upgrade tensorflow-2.1.0-cp36-cp36m-linux_x86_64.whl
RUN rm -f tensorflow-2.1.0-cp36-cp36m-linux_x86_64.whl

#ENTRYPOINT /srv/entry-point.sh
ENTRYPOINT bash


