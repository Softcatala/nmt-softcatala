pushd ../..
docker build -t translate-service . -f serving/translate-service/Dockerfile
popd
docker image ls | grep translate-service
