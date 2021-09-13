FROM python:3.8.2-slim-buster as generate_data

RUN apt-get update && apt-get -y upgrade && apt-get install wget unzip -y --no-install-recommends

RUN mkdir models
WORKDIR models

ENV URL https://www.softcatala.org/pub/softcatala/opennmt/models/

ENV FILE eng-cat-2021-08-22.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d eng-cat/

ENV FILE cat-eng-2021-08-22.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d cat-eng/

ENV FILE deu-cat-2021-08-11.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d deu-cat/

ENV FILE cat-deu-2021-08-12.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d cat-deu/

RUN rm *.zip

FROM python:3.8.2-slim-buster
COPY --from=generate_data /models/ /srv/models/

ENTRYPOINT bash
