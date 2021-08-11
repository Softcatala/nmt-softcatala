FROM python:3.8.2-slim-buster as generate_data

RUN apt-get update && apt-get -y upgrade && apt-get install wget unzip -y --no-install-recommends

RUN mkdir models
WORKDIR models

RUN wget -q https://www.softcatala.org/pub/softcatala/opennmt/models/eng-cat-2021-08-09.zip && \
    unzip eng-cat-2021-08-09.zip -x tensorflow/* -d eng-cat/
RUN wget -q https://www.softcatala.org/pub/softcatala/opennmt/models/cat-eng-2021-08-10.zip && \
    unzip cat-eng-2021-08-10.zip -x tensorflow/* -d cat-eng/
RUN wget -q https://www.softcatala.org/pub/softcatala/opennmt/models/deu-cat-2021-08-11.zip && \
    unzip deu-cat-2021-08-11.zip -x deu-cat/tensorflow/* -d deu-cat/
RUN wget -q https://www.softcatala.org/pub/softcatala/opennmt/models/cat-deu-2021-04-22.zip && \
    unzip cat-deu-2021-04-22.zip -x cat-deu/tensorflow/* -d .

RUN rm *.zip

FROM python:3.8.2-slim-buster
COPY --from=generate_data /models/ /srv/models/

ENTRYPOINT bash
