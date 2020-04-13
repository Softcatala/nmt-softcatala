#FROM python:3.6.9-buster as generate_data
FROM opennmt/tensorflow-serving:2.1.0

RUN apt-get update && apt-get install wget vim curl git software-properties-common -y --no-install-recommends
RUN apt install python-dev python-pip -y

RUN pip install pip six numpy wheel setuptools mock 'future>=0.17.1' && \
    pip install keras_applications --no-deps && \
    pip install keras_preprocessing --no-deps

RUN wget https://github.com/bazelbuild/bazelisk/releases/download/v1.2.1/bazelisk-linux-amd64 -q && \
    mv bazelisk-linux-amd64 /bin/bazel && \
    chmod +x /bin/bazel

RUN wget https://github.com/tensorflow/tensorflow/archive/v2.1.0.tar.gz -q 
RUN tar -xf v2.1.0.tar.gz
WORKDIR tensorflow-2.1.0 

RUN ./configure
RUN bazel build -c opt --copt=-mavx --copt=-mavx512f --copt=-mavx2 --copt=-mfma --config=opt //tensorflow/tools/pip_package:build_pip_package
RUN ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg

ENTRYPOINT bash


