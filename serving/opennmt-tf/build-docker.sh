pushd ../..
docker build -t opennmt-tf . -f serving/opennmt-tf/Dockerfile
popd
docker image ls | grep opennmt-tf


