FROM python:3.8.2-slim-buster as generate_data

RUN apt-get update && apt-get -y upgrade && apt-get install wget unzip -y --no-install-recommends

RUN mkdir models
WORKDIR models

ENV URL https://www.softcatala.org/pub/softcatala/opennmt/models/

# Production

ENV FILE eng-cat-2021-08-22.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d eng-cat/

ENV FILE cat-eng-2021-08-22.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d cat-eng/

ENV FILE deu-cat-2021-08-11.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d deu-cat/

ENV FILE cat-deu-2021-08-12.zip
RUN wget -q $URL/$FILE && unzip $FILE -x tensorflow/* -d cat-deu/

# Development

ENV FILE cat-fra-2021-09-05-1630884602.zip
RUN wget -q $URL/baseline/$FILE && unzip $FILE -x tensorflow/* -d cat-fra/

ENV FILE cat-ita-2021-09-06-1630941629.zip
RUN wget -q $URL/baseline/$FILE && unzip $FILE -x tensorflow/* -d cat-ita/

ENV FILE cat-nld-2021-09-07-1631052167.zip
RUN wget -q $URL/baseline/$FILE && unzip $FILE -x tensorflow/* -d cat-nld/

ENV FILE cat-spa-2021-09-06-1630913216.zip
RUN wget -q $URL/baseline/$FILE && unzip $FILE -x tensorflow/* -d cat-spa/

ENV FILE fra-cat-2021-09-04-1630729544.zip
RUN wget -q $URL/baseline/$FILE && unzip $FILE -x tensorflow/* -d fra-cat/

ENV FILE ita-cat-2021-09-03-1630696965.zip
RUN wget -q $URL/baseline/$FILE && unzip $FILE -x tensorflow/* -d ita-cat/

ENV FILE nld-cat-2021-09-07-1631023781.zip
RUN wget -q $URL/baseline/$FILE && unzip $FILE -x tensorflow/* -d nld-cat/

ENV FILE spa-cat-2021-09-03-1630697264.zip
RUN wget -q $URL/baseline/$FILE && unzip $FILE -x tensorflow/* -d spa-cat/


RUN rm *.zip

FROM python:3.8.2-slim-buster
COPY --from=generate_data /models/ /srv/models/

ENTRYPOINT bash
