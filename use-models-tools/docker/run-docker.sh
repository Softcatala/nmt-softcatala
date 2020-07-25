DIRECTORY=/home/jordi/sc/OpenNMT/nmt-softcatala/use-models-tools/
COMMAND_LINE='-f ca.po'
docker run -it -v $DIRECTORY:/srv/files/ --env FILE_TYPE='po' --env COMMAND_LINE="$COMMAND_LINE" --rm use-model-tools --name use-model-tools

