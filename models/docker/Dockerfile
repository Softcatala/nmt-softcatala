FROM python:3.8.2-slim-buster as generate_data

RUN apt-get update && apt-get -y upgrade && apt-get install wget unzip -y --no-install-recommends

RUN mkdir models
WORKDIR models

ENV URL https://www.softcatala.org/pub/softcatala/opennmt/models/

ENV FILE spa-cat-2021-08-31-1630414931.zip
RUN wget -q $URL/beta/$FILE && unzip $FILE -x tensorflow/* -d spa-cat/

ENV FILE fra-cat-2021-08-30-1630334880.zip
RUN wget -q $URL/beta/$FILE && unzip $FILE -x tensorflow/* -d fra-cat/

ENV FILE eng-cat-2021-08-22.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d eng-cat/

ENV FILE cat-eng-2021-08-22.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d cat-eng/

ENV FILE deu-cat-2021-08-31-1630380073.zip
RUN wget -q $URL/beta/$FILE && unzip $FILE -x tensorflow/* -d deu-cat/

ENV FILE cat-deu-2021-08-12.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d cat-deu/

RUN rm *.zip

FROM python:3.8.2-slim-buster
COPY --from=generate_data /models/ /srv/models/

ENTRYPOINT bash
