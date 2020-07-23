#cat ../input.txt | docker run -i use-model-tools --rm use-model-tools
cat ../input.po | docker run --env FILE_TYPE='po' -i use-model-tools --rm use-model-tools 


