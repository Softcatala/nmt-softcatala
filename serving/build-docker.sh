echo Builds an image using Tensorflow 2.0 and the models at models/eng-cat/
pushd ..
docker build -t traductor-eng-cat . -f serving/Dockerfile
popd
docker image ls | grep traductor-eng-cat
