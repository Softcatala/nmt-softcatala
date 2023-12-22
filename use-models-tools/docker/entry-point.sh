#!/bin/bash

#COMMAND_LINE="-f flores200.eng -t output.cat -m eng-cat"


#docker run --env "DEVICE=cpu" --env "COMPUTE_TYPE=int8" --env "DEVICE_INDEX=0"   --gpus 0  -it registry.softcatala.org/github/nmt-softcatala/use-models-tools:test-whisper

cd /srv/flores
/usr/bin/time -f %U whisper-ctranslate2 15GdH1.mp3  --model medium --threads 8 --device $DEVICE --compute_type $COMPUTE_TYPE --device_index $DEVICE_INDEX
