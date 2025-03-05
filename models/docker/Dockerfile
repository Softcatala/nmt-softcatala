FROM python:3.12.9-slim-bookworm as generate_data

RUN apt-get update && apt-get -y upgrade && apt-get install wget unzip -y --no-install-recommends

RUN mkdir models
WORKDIR models

ENV URL https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22

ENV FILE cat-deu-2024-10-06.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-eng-2024-09-29.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-eus-2024-08-12.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-fra-2024-08-30.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-glg-2024-09-04.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-ita-2024-08-30.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-jpn-2024-10-08.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-nld-2022-11-19.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-oci-2022-11-21.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE cat-por-2022-11-18.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

#ENV FILE cat-spa-2022-11-17.zip
#RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE deu-cat-2024-10-02.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE eng-cat-2024-09-24.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE eus-cat-2024-08-09.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE fra-cat-2024-08-29.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE glg-cat-2024-09-03.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE ita-cat-2024-08-29.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE jpn-cat-2024-10-04.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE nld-cat-2022-11-19.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE oci-cat-2022-11-17.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

ENV FILE por-cat-2022-11-16.zip
RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

#ENV FILE spa-cat-2022-11-16.zip
#RUN wget -q $URL/$FILE && unzip $FILE -x */tensorflow/*

RUN rm *.zip

FROM python:3.12.9-slim-bookworm
COPY --from=generate_data /models/ /srv/models/

ENTRYPOINT bash
