FROM python:3.8.6-slim-buster as generate_data

COPY serving/translate-batch/requirements.txt /srv/
COPY serving/translate-batch/*.py /srv/
COPY serving/translate-batch/segment.srx /srv/
COPY serving/translate-batch/docker/entry-point.sh /srv/

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


FROM python:3.8.6-slim-buster

RUN apt-get update && apt-get -y upgrade && apt-get install vim -y --no-install-recommends
RUN apt-get install python3-pip -y --no-install-recommends
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

COPY --from=generate_data /srv/ /srv/

WORKDIR /srv
RUN pip3 install -r requirements.txt

ENTRYPOINT /srv/entry-point.sh
#ENTRYPOINT bash
