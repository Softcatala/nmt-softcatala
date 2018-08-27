# Introduction

This repository contains Neural Machine Translation proof of concepts done at Softcatalà

Test have been done with https://github.com/OpenNMT/OpenNMT-tf

# Runing the models

## Models

We have created two models:

* 1532515736 (https://www.softcatala.org/pub/softcatala/opennmt-models/1532307246.zip)
  * This model is build using Softcatalà translations only 
  * Total number of sentences: 190523
  * replace_unknown_target: yes
  * model: NMTSmall
  * BLEU = 30.50

* 1532307246 (https://www.softcatala.org/pub/softcatala/opennmt-models/1532515736.zip)
  * This model is build using all translations that we have
  * Total number of sentences: 566699
  * replace_unknown_target: no
  * model: NMTSmall
  * BLEU = 29.97

## Samples

Examples of how new files (not previous part of the training corpus) how they look like with different models:

https://github.com/jordimas/nmt-softcatala/tree/master/translations

## Translating a new PO file

Code is at ApplyToPoFile subdirectory

* Install TensorFlow serving
* Run ```run-model-sever.sh``` (server)
* Run ```python3 ApplyToPoFile PO_file```

By default all strings are marked as fuzzy

# Building the models

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

onmt-main train_and_eval --model_type NMTSmall --config config/opennmt-defaults.yml config/data/toy-ende.yml

# Contact

Email address: Jordi Mas: jmas@softcatala.org
