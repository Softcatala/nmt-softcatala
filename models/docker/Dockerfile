FROM python:3.8.2-slim-buster as generate_data

RUN apt-get update && apt-get -y upgrade && apt-get install wget unzip -y --no-install-recommends

RUN mkdir models
WORKDIR models

ENV URL https://www.softcatala.org/pub/softcatala/opennmt/models/

ENV FILE cat-deu-2021-09-30.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d cat-deu/

ENV FILE cat-eng-2021-09-29.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d cat-eng/

ENV FILE cat-fra-2021-09-28.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d cat-fra/

ENV FILE cat-ita-2021-09-27.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d cat-ita/

ENV FILE cat-nld-2021-09-30.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d cat-nld/

ENV FILE cat-por-2021-09-29.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d cat-por/

ENV FILE cat-spa-2021-09-28.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d cat-spa/

ENV FILE deu-cat-2021-09-27.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d deu-cat/

ENV FILE eng-cat-2021-09-26.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d eng-cat/

ENV FILE fra-cat-2021-09-24.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d fra-cat/

ENV FILE ita-cat-2021-09-23.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d ita-cat/

ENV FILE nld-cat-2021-09-27.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d nld-cat/

ENV FILE por-cat-2021-09-25.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d por-cat/

ENV FILE spa-cat-2021-09-25.zip
RUN wget -q $URL/2021-09-30/$FILE && unzip $FILE -x tensorflow/* -d spa-cat/

RUN rm *.zip

FROM python:3.8.2-slim-buster
COPY --from=generate_data /models/ /srv/models/

ENTRYPOINT bash
