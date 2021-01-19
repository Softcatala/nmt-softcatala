echo "Translating tatoeba"
docker run -it -v "$(pwd)":/srv/files/ --env CTRANSLATE_BEAM_SIZE=2 --env COMMAND_LINE="-f input/tatoeba.en-ca.en -t translated/tatoeba-opennmt-ca.txt -m eng-cat" --rm use-models-tools --name use-models-tools

echo "Translating sleepyhollow"
docker run -it -v "$(pwd)":/srv/files/ --env CTRANSLATE_BEAM_SIZE=2 --env COMMAND_LINE="-f input/sleepyhollow.en-ca.en -t translated/sleepyhollow-opennmt-ca.txt -m eng-cat" --rm use-models-tools --name use-models-tools

echo "Translating sc-users"
docker run -it -v "$(pwd)":/srv/files/ --env CTRANSLATE_BEAM_SIZE=2 --env COMMAND_LINE="-f input/sc-users-ca.txt -t translated/sc-users-opennmt-ca.txt -m eng-cat" --rm use-models-tools --name use-models-tools

echo "Translating federalist"
docker run -it -v "$(pwd)":/srv/files/ --env CTRANSLATE_BEAM_SIZE=2 --env COMMAND_LINE="-f input/federalist.en-ca.en -t translated/federalist-opennmt-ca.txt -m eng-cat" --rm use-models-tools --name use-models-tools


