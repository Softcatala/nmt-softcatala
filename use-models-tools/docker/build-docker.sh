pushd ../..
docker build -t use-model-tools . -f use-models-tools/docker/Dockerfile
popd
docker image ls | grep use-model-tools
