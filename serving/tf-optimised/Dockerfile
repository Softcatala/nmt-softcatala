#FROM python:3.6.9-buster
FROM opennmt/tensorflow-serving:2.1.0

RUN apt-get update && apt-get -y upgrade && apt-get install wget vim curl git software-properties-common -y --no-install-recommends
RUN apt install python3-dev python3-pip -y
RUN pip3 install --upgrade pip && pip3 install --upgrade setuptools

RUN pip3 install pip six numpy wheel setuptools mock 'future>=0.17.1' && \
    pip3 install keras_applications --no-deps && \
    pip3 install keras_preprocessing --no-deps

RUN wget https://github.com/bazelbuild/bazelisk/releases/download/v1.2.1/bazelisk-linux-amd64 -q && \
    mv bazelisk-linux-amd64 /bin/bazel && \
    chmod +x /bin/bazel

RUN wget https://github.com/tensorflow/tensorflow/archive/v2.1.0.tar.gz -q 
RUN tar -xf v2.1.0.tar.gz
WORKDIR tensorflow-2.1.0 

RUN ln -s /usr/bin/python3 /usr/bin/python	
RUN ./configure
RUN bazel build -c opt --copt=-mavx --copt=-mavx512f --copt=-mavx2 --copt=-mfma --config=opt --noincompatible_strict_action_env //tensorflow/tools/pip_package:build_pip_package
RUN ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

ENTRYPOINT bash


