pushd ../../..
docker build -t translate-service-test . -f serving/translate-service/docker/Dockerfile-test
popd
docker image ls | grep translate-service-test
