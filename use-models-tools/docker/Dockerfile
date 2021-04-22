FROM python:3.8.2-slim-buster

RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY use-models-tools/requirements.txt /srv/
WORKDIR /srv
RUN pip3 install -r requirements.txt

COPY use-models-tools/*.py /srv/
COPY use-models-tools/segment.srx /srv/
COPY use-models-tools/docker/entry-point.sh /srv/

COPY models/eng-cat/ctranslate2/ /srv/models/eng-cat/ctranslate2/
COPY models/eng-cat/tokenizer/ /srv/models/eng-cat/tokenizer/
COPY models/eng-cat/metadata/model_description.txt /srv/models/eng-cat/metadata/

COPY models/cat-eng/ctranslate2/ /srv/models/cat-eng/ctranslate2/
COPY models/cat-eng/tokenizer/ /srv/models/cat-eng/tokenizer/
COPY models/cat-eng/metadata/model_description.txt /srv/models/cat-eng/metadata/

COPY models/deu-cat/ctranslate2/ /srv/models/deu-cat/ctranslate2/
COPY models/deu-cat/tokenizer/ /srv/models/deu-cat/tokenizer/
COPY models/deu-cat/metadata/model_description.txt /srv/models/deu-cat/metadata/

COPY models/cat-deu/ctranslate2/ /srv/models/cat-deu/ctranslate2/
COPY models/cat-deu/tokenizer/ /srv/models/cat-deu/tokenizer/
COPY models/cat-deu/metadata/model_description.txt /srv/models/cat-deu/metadata/


COPY models/deu-cat/ctranslate2/ /srv/models/deu-cat/
#COPY models/cat-deu/ctranslate2/ /srv/models/cat-deu/
COPY models/deu-cat/tokenizer/*.model /srv/models/tokenizer/

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash
