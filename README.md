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

* Softcatalà memories model (https://www.softcatala.org/pub/softcatala/opennmt/models/sc-memories-2020-03-29.zip)
  * This model is build using Softcatalà translations only
  * Total number of sentences: 195532
  * replace_unknown_target: yes
  * model: Transformer
  * Tokenizer: SentencePiece
  * BLEU = 43.24
  * Default if no specified otherwise

* English - Catalan model (https://www.softcatala.org/pub/softcatala/opennmt/models/eng-cat-2020-04-11.zip)
  * Total number of sentences: 4426107
  * replace_unknown_target: yes
  * model: Transformer
  * Tokenizer: SentencePiece
  * BLEU = 40.12
  * Default if no specified otherwise

* Catalan - English model (https://www.softcatala.org/pub/softcatala/opennmt/models/cat-eng-2020-04-12.zip)
  * Total number of sentences: 4426107
  * replace_unknown_target: yes
  * model: Transformer
  * Tokenizer: SentencePiece
  * BLEU = 40.36
  * Default if no specified otherwise

The corpus used to train this model can be obtain from the trainings-sets directory executing these scripts:

* *get.sh* gets all the raw files
* *preprocess.sh* that does the necessary preprocessing of the data

# Serving the models in local (non-production environments)

## Install TensorFlow Serving

Pull this Docker image:

```
docker pull opennmt/tensorflow-serving:2.1.0
```

This is a standard TensorFlow Docker image that also contains Addons>GatherTree addon needed by OpenNMT-tf generated models.

## Running TensorFlow Serving

You can download the model into the Docker host and mapped it inside the container.

For example if you download 'https://gent.softcatala.org/jmas/files/model-sc-2020-03-29-1585459573.zip' at 'nmt-softcatala/models/model-sc'

```
cd nmt-softcatala

docker run -t --rm -p 8501:8501 -p 8500:8500 \
    -v "$PWD/models/model-sc:/models/model-sc" \
    -e MODEL_NAME=model-sc \
    opennmt/tensorflow-serving:2.1.0  --enable_batching=true
```

Note: you need to map 8501 ports (gRPC) and 8500 (REST)


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

Code is in ApplyToPoFile subdirectory. For example to translate the file 'test.po' with the 'model-sc'

* Run ```python3 model-to-po.py -f test.po -m model-sc```

By default all strings translated by the translation system are marked as 'fuzzy'

## Translating a plain text file

* Run ```python3 model-to-txt.py --help``` for all details


# Contact

Email address: Jordi Mas: jmas@softcatala.org
