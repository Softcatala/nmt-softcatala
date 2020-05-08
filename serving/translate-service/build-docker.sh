pushd ../..
docker build -t traductor-eng-cat . -f serving/translate-service/Dockerfile
popd
docker image ls | grep traductor-eng-cat
