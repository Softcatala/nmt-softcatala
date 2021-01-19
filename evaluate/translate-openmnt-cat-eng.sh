docker run -it -v "$(pwd)":/srv/files/ --env CTRANSLATE_BEAM_SIZE=2 --env COMMAND_LINE="-f input/tatoeba.en-ca.ca -t translated/tatoeba-opennmt-en.txt -m cat-eng" --rm use-models-tools --name use-models-tools

docker run -it -v "$(pwd)":/srv/files/ --env CTRANSLATE_BEAM_SIZE=2 --env COMMAND_LINE="-f input/sleepyhollow.en-ca.ca -t translated/sleepyhollow-opennmt-en.txt -m cat-eng" --rm use-models-tools --name use-models-tools

docker run -it -v "$(pwd)":/srv/files/ --env CTRANSLATE_BEAM_SIZE=2 --env COMMAND_LINE="-f input/sc-users-ca.txt -t translated/sc-users-opennmt-en.txt -m cat-eng" --rm use-models-tools --name use-models-tools


