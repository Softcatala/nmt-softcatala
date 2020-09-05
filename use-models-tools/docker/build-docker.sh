pushd ../..
docker build -t use-models-tools . -f use-models-tools/docker/Dockerfile
popd
docker image ls | grep use-models-tools
