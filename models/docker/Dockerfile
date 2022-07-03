FROM python:3.10.4-slim-bullseye as generate_data

RUN apt-get update && apt-get -y upgrade && apt-get install wget unzip -y --no-install-recommends

RUN mkdir models
WORKDIR models

ENV URL https://www.softcatala.org/pub/softcatala/opennmt/models/

ENV FILE cat-deu-2022-06-25.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-eng-2022-06-24.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-fra-2022-06-25.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-ita-2022-06-26.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-jpn-2022-07-02.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-nld-2022-06-29.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-por-2022-06-28.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

#ENV FILE cat-spa-2022-06-27.zip
#RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE deu-cat-2022-06-19.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE eng-cat-2022-06-18.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE fra-cat-2022-06-20.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE ita-cat-2022-06-21.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE jpn-cat-2022-06-29.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE nld-cat-2022-06-23.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE por-cat-2022-06-22.zip
RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

#ENV FILE spa-cat-2022-06-21.zip
#RUN wget -q $URL/2022-06-17/$FILE && unzip $FILE -x */tensorflow/*

RUN rm *.zip

FROM python:3.10.4-slim-bullseye
COPY --from=generate_data /models/ /srv/models/

ENTRYPOINT bash
