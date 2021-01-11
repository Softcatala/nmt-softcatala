pushd ../../..
docker build -t translate-service . -f serving/translate-service/docker/Dockerfile
popd
cat ../../../models/cat-eng/metadata/model_description.txt  |grep -w "Model description"
cat ../../../models/eng-cat/metadata/model_description.txt  | grep -w "Model description"
docker image ls | grep translate-service
