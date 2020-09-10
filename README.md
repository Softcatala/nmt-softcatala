# Introduction

This repository contains Neural Machine Translation tools and models built at Softcatalà using [OpenNMT-tf 2](https://github.com/OpenNMT/OpenNMT-tf) and [TensorFlow 2](https://www.tensorflow.org/)

# Description of the directories

* *data-processing-tools*: set of data processing tools that convert for different formats to OpenNMT plain text input format
* *serving*: contains a microservice that provides a basic transtion API calling TensorFlow serving.
* *use-models-tools*: contains tools to use the models to translate text files or PO files
* *evaluate*: set of tools and corpus to evaluatate diferent translation systems
* *quality*: set of corpus to evaluate the quality of the 'eng-cat' model only


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


The corpus used to train this model can be obtain from the trainings-sets directory executing these scripts:

* *get.sh* gets all the raw files
* *preprocess.sh* that does the necessary preprocessing of the data

# Serving the models in local (non-production environments)

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


# Serving the models in production

Our tentative approach to run these models in production is:

* Leverage on a standard OpenNMT Docker image
* Include our own model data
* Include our own microservice (see [/serving](./serving)) to serve translations based on the model

To build the container to be use in production execute:

```
cd serving
./build-docker.sh
```
To execute it:

```
cd serving
./run-docker.sh
```

and to test it:

http://localhost:8700/translate/?text=hello

# Using the models

This is assumes that you are already serving the models.

## Translating a new PO file using the a model

Code is in ApplyToPoFile subdirectory. For example to translate the file 'test.po':

* Run ```python3 model-to-po.py -f test.po```

By default all strings translated by the translation system are marked as 'fuzzy'

## Translating a plain text file

* Run ```python3 model-to-txt.py --help``` for all details

# How to help?

See [here](./CONTRIBUTING.md) (In Catalan)

# Contact

Email address: Jordi Mas: jmas@softcatala.org
