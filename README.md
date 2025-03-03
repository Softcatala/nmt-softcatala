# Introduction

This repository contains Neural Machine Translation tools and models built at Softcatalà using [OpenNMT-tf 2](https://github.com/OpenNMT/OpenNMT-tf) and [TensorFlow 2](https://www.tensorflow.org/)

# Description of the directories

* *data-processing-tools*: set of data processing tools that convert for different formats to OpenNMT plain text input format
* *serving*: contains a microservice that provides a translation API for web service and batch file processing.
* *use-models-tools*: contains tools to use the models to translate text files or PO files
* *evaluate*: set of tools and corpus to evaluate different translation systems (including BLEU scores)
* *training*: scripts and configurations to train the models

# Models

All the Softcatalà built models are available here: https://github.com/Softcatala/nmt-models

# Serving

## Requirements

You need [Docker](https://www.docker.com/) and [Make](https://www.gnu.org/software/make/) for which there are different implementations depending on your operating system.

## Serving the models in production

You can build and run the docker translation service:

* Build the solution ```make build-all```
* Run ```make docker-run-translate-service```
* Open in your browser ```http://localhost:8700/translate?langpair=en|ca&q=Hello!```

To run exactly the system in production you also need ```docker-compose```. You can execute it by running:

* ```make docker-run-all-services```


## Apertium API

One of the use cases for Machine Translation is to use it to speed up the work of translators.

In order to integrate easily with already existing translation tools we support the [Apertium Web API](https://wiki.apertium.org/wiki/Apertium-apy). This means that you can use any tool that has support for Apertium.

We confirm that the following tools work using Apertium pluggins:

* Okapi Framework
* OmegaT translation plugin

**Supported methods**

| Method | Verb
|---|---|
|/translate  | GET or POST
|/listLanguageNames  | GET
|/listPairs  | GET

# Using the models in your machine

This is useful for example if you want to translate large volumes using our prebuild English - Catalan models using the same exact version that we have in production:

* Build command line tool ```make docker-build-use-models-tools```

To test quickly that everything works:
* ```echo "Hello World" > input.txt```
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f input.txt -t output.txt -m eng-cat" --rm use-models-tools --name use-models-tools```
* ```more output.txt```

To translate PO files:
* File ```ca.po``` is your current directory
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f ca.po -m eng-cat" --env FILE_TYPE='po' --rm use-models-tools --name use-models-tools```

The translated file will be ```ca.po-ca.po```

To translate a text file from Catalan to English:
* ```echo "Hola món" > input.txt```
* ```docker run -it -v "$(pwd)":/srv/files/ --env COMMAND_LINE="-f input.txt -t output.txt -m cat-eng" --rm use-models-tools --name use-models-tools```
* ```more output.txt```

Note: that the parameter ```-m cat-eng``` indicates the translation model to use.

# Development

## Performance test of the translation service

It is important to understand that there are no major performance regressions.

Install the ```wrk``` performance testing tool by using ```sudo apt-get install wrk```

Follow these steps:
* Run ```make docker-run-all-services``` to run all the services for the performance test
* Use ```serving/perf-tests``` script to run the performance test

# License

See [license](./LICENSE.md)

# Contact

Email address: Jordi Mas: jmas@softcatala.org
