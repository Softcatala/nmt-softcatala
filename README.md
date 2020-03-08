# Introduction

This repository contains Neural Machine Translation models built at Softcatalà using [OpenNMT-tf 2.00](https://github.com/OpenNMT/OpenNMT-tf) and [TensorFlow 2.0](https://www.tensorflow.org/)

# Models

We have created the following models:

* Model SC (https://gent.softcatala.org/jmas/files/model-sc-20200308.zip)
  * This model is build using Softcatalà translations only (all source files are at training-sets/sc)
  * Total number of sentences: 195532
  * replace_unknown_target: yes
  * model: Transformer
  * BLEU = 42.80
  * Default if no specified otherwise

## Samples

Examples of how new files (not previous part of the training corpus) look when translated with these models:

https://github.com/jordimas/nmt-softcatala/tree/master/translations

# Using the models

## Install TensorFlow Serving

Pull this Docker image:

```
docker pull opennmt/tensorflow-serving:2.1.0
```

This is a standard TensorFlow Docker image that also contains Addons>GatherTree addon needed by OpenNMT-tf generated models.

## Running TensorFlow Serving

You can download the model into the Docker host and mapped it inside the container.

For example if you download 'https://gent.softcatala.org/jmas/files/model-sc-20200308.zip' at 'nmt-softcatala/models/model-sc'

```
cd nmt-softcatala

docker run -t --rm -p 8501:8501 -p 8500:8500 \
    -v "$PWD/models/model-sc:/models/model-sc" \
    -e MODEL_NAME=model-sc \
    opennmt/tensorflow-serving:2.1.0  --enable_batching=true
```

Note: you need to map 8501 ports (gRPC) and 8500 (REST)


## Translating a new PO file using the a model

Code is in ApplyToPoFile subdirectory. For example to translate the file 'test.po' with the 'model-sc'

* Run ```python3 ApplyToPoFile test.po model-sc```

By default all strings translated by the translation system are marked as 'fuzzy'

# Building the models (if you do not want to use provided models)

## Building a OpenNMT corpus from PO files

* Download Softcatalà translation memory:
https://www.softcatala.org/recursos/memories/softcatala-tm.po.zip

* Run PoToOpenNMT/converter.py

This produce 6 files:
* src-test.txt - Source file used to test the model
* tgt-test.txt - Target file used to test the model
* src-train.txt - Source file used to train the model
* tgt-train.txt - Target file used to train the model
* src-val.txt - Source file used to validate the model
* tgt-val.txt - Target file used to validate the model

These files should be copied

## Build model

1\. Build the word vocabularies:

```
onmt-build-vocab --size 50000 --save_vocab src-vocab.txt src-train.txt
onmt-build-vocab --size 50000 --save_vocab tgt-vocab.txt tgt-train.txt
```

2\. Train with preset parameters:

```
onmt-main --model_type Transformer --config data.yml --auto_config train --with_eval
```

3\. Translate a test file with the latest checkpoint and show Bleu:

```
onmt-main --config data.yml --auto_config infer --features_file src-test.txt > predictions.txt
perl ../OpenNMT-py/tools/multi-bleu.perl tgt-test.txt < predictions.txt
```

# Contact

Email address: Jordi Mas: jmas@softcatala.org
