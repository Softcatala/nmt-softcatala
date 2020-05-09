pushd ../..
docker build -t translate-batch . -f serving/translate-batch/Dockerfile
popd
docker image ls | grep translate-batch
