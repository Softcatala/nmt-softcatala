# Introduction

This repository contains Neural Machine Translation tools and models built at Softcatalà using [OpenNMT-tf 2](https://github.com/OpenNMT/OpenNMT-tf) and [TensorFlow 2](https://www.tensorflow.org/)

# Description of the directories

* *data-processing-tools*: set of data processing tools that convert for different formats to OpenNMT plain text input format
* *serving*: contains a microservice that provides a transtion API for web service and batch file processing.
* *use-models-tools*: contains tools to use the models to translate text files or PO files
* *evaluate*: set of tools and corpus to evaluatate diferent translation systems (including BLEU scores)
* *training*: scrips and configurations to train the models

# Models

## Softcatalà built models

We have created the following models:

* English - Catalan model (https://www.softcatala.org/pub/softcatala/opennmt/models/eng-cat-2021-08-09.zip)
  * Total number of sentences: 4602069
  * model: TransformerRelative
  * Tokenizer: SentencePiece
  * BLEU = 41.44

* Catalan - English model (https://www.softcatala.org/pub/softcatala/opennmt/models/cat-eng-2021-08-10.zip)
  * Total number of sentences: 4602069
  * model: TransformerRelative
  * Tokenizer: SentencePiece
  * BLEU = 42.60

* German - Catalan model (https://www.softcatala.org/pub/softcatala/opennmt/models/deu-cat-2021-08-11.zip)
  * Total number of sentences: 3262424
  * model: TransformerRelative
  * Tokenizer: SentencePiece
  * BLEU = 33.65

* Catalan - German model (https://www.softcatala.org/pub/softcatala/opennmt/models/cat-deu-2021-08-12.zip)
  * Total number of sentences: 3262424
  * model: TransformerRelative
  * Tokenizer: SentencePiece
  * BLEU = 27.02

The corpus that we used for training are available at https://www.softcatala.org/pub/softcatala/opennmt/training-sets/ and https://github.com/Softcatala/parallel-catalan-corpus/

### Structure of the models

Description of the directories on the contained in the models zip file:

* *tensorflow*: model exported in Tensorflow format
* *ctranslate2*: model exported in CTranslate2 format (used for inference)
* *metadata*: description of the model
* *tokenizer*: SentencePiece models for both languages

# Serving

## Serving the models in production

You can build and run the docker that we use in production:

* Build models ```cd models/docker/ && ./build-docker.sh```
* Build serving ```cd serving/translate-service/docker/ && ./build-docker.sh```
* Run ```docker run -it --rm -p 8700:8700 translate-service```
* Open in your browser ```http://localhost:8700/translate?langpair=en|ca&q=Hello!```

## Apertium API

One of the use cases for Machine Translation is to use it to speed up the work of translators.

In order to integrate easily with already existing translation tools we support the [Apertium Web API](https://wiki.apertium.org/wiki/Apertium-apy). This means that you can use any tool that has support for Apertium.

We confirm that the following tools work using Apertium pluggins:

* Okapi Framework
* OmegaT translation plugin
* Gedit's Apertium plugin

**Supported methods**

| Method | Verb
|---|---|
|/translate  | GET or POST
|/listLanguageNames  | GET
|/listPairs  | GET

# Using the models in your machine

This is useful for example if you want to translate large volumes using our prebuild English - Catalan models using the same exact version that we have in production:

* Build models ```cd models/docker/ && ./build-docker.sh```
* Build serving ```cd use-models-tools/docker && ./build-docker.sh```

To test quickly that every works:
* ```echo "Hello World" > input.txt```
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f input.txt -t output.txt" --rm use-models-tools --name use-models-tools```
* ```more output.txt```

To translate PO files:
* File ```ca.po``` is your current directory
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f ca.po" --env FILE_TYPE='po' --rm use-models-tools --name use-models-tools```

The translated file will be ```ca.po-ca.po```

To translate a text file from Catalan to English:
* ```echo "Hola món" > input.txt```
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f input.txt -t output.txt -m cat-eng" --rm use-models-tools --name use-models-tools```
* ```more output.txt```

# License

See [license](./LICENSE.md)

# How to help?

See [here](./CONTRIBUTING.md) (In Catalan)

# Contact

Email address: Jordi Mas: jmas@softcatala.org
