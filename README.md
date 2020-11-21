# Introduction

This repository contains Neural Machine Translation tools and models built at Softcatalà using [OpenNMT-tf 2](https://github.com/OpenNMT/OpenNMT-tf) and [TensorFlow 2](https://www.tensorflow.org/)

# Description of the directories

* *data-processing-tools*: set of data processing tools that convert for different formats to OpenNMT plain text input format
* *serving*: contains a microservice that provides a basic transtion API calling TensorFlow serving.
* *use-models-tools*: contains tools to use the models to translate text files or PO files
* *evaluate*: set of tools and corpus to evaluatate diferent translation systems
* *training*: scrips and configurations to train the models

# Models

## Softcatalà built models

We have created the following models:

* English - Catalan model (https://www.softcatala.org/pub/softcatala/opennmt/models/eng-cat-2020-09-09.zip)
  * Total number of sentences: 4602069
  * replace_unknown_target: yes
  * model: Transformer
  * Tokenizer: SentencePiece
  * BLEU = 41.93
  * Default if no specified otherwise

* Catalan - English model (https://www.softcatala.org/pub/softcatala/opennmt/models/eng-cat-2020-09-09.zip)
  * Total number of sentences: 4602069
  * replace_unknown_target: yes
  * model: Transformer
  * Tokenizer: SentencePiece
  * BLEU = 41.29
  * Default if no specified otherwise

### Structure of the models

Description of the directories on the contained in the models zip file:

* *tensorflow*: model exported in Tensorflow format
* *ctranslate2*: model exported in CTranslate2 format (used for inference)
* *metadata*: description of the model
* *tokenizer*: SentencePiece models for both languages

# Serving

## Serving the models in production

You can download the docker that we use in production

* Type ```docker pull jordimash/translate-service:v18``` (check if there are newer versions of the [tag](https://hub.docker.com/repository/docker/jordimash/translate-service))
* docker run  -it --rm -p 8700:8700 jordimash/translate-service:v18
* http://localhost:8700/translate?langpair=en|cat&q=Hello!

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

This is useful for example if you want to translate large volumes using our prebuild English - Catalan models using the same exact version that we have in production.

* You need Docker installed in your system

* Type ```docker pull jordimash/use-models-tools```

To test quickly that every works:
* ```echo "Hello World" > input.txt```
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f input.txt -t output.txt" --rm jordimash/use-models-tools --name jordimash/use-models-tools```
* ```more output.txt```

To translate PO files:
* File ```ca.po``` is your current directory
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f ca.po" --env FILE_TYPE='po' --rm jordimash/use-models-tools --name jordimash/use-models-tools```

The translated file will be ```ca.po-ca.po```

To translate a text file from Catalan to English:
* ```echo "Hola món" > input.txt```
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f input.txt -t output.txt -m cat-eng" --rm jordimash/use-models-tools --name jordimash/use-models-tools```
* ```more output.txt```

# License

See [license](./LICENSE.md)

# How to help?

See [here](./CONTRIBUTING.md) (In Catalan)

# Contact

Email address: Jordi Mas: jmas@softcatala.org
