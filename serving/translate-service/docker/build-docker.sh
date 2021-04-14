pushd ../../..
docker build -t translate-service . -f serving/translate-service/docker/Dockerfile
popd
cat ../../../models/cat-eng/metadata/model_description.txt | grep -e "Model description" -e "Date" && echo -e "\r"
cat ../../../models/eng-cat/metadata/model_description.txt | grep -e "Model description" -e "Date" && echo -e "\r"
cat ../../../models/deu-cat/metadata/model_description.txt | grep -e "Model description" -e "Date" && echo -e "\r"
docker image ls | grep translate-service
