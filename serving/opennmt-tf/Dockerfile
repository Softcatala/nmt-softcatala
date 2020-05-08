FROM opennmt/tensorflow-serving:2.1.0

EXPOSE 8500
EXPOSE 8501

COPY models/eng-cat/ models/eng-cat/
COPY models/cat-eng/ models/cat-eng/
RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends

RUN mkdir /srv
COPY serving/opennmt-tf/tf-optimised/tensorflow-2.1.0-cp36-cp36m-linux_x86_64.whl /srv/

RUN pip3 install --ignore-installed --upgrade tensorflow-2.1.0-cp36-cp36m-linux_x86_64.whl
RUN rm -f tensorflow-2.1.0-cp36-cp36m-linux_x86_64.whl

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash


