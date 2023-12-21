#!/bin/bash

#COMMAND_LINE="-f flores200.eng -t output.cat -m eng-cat"


cd /srv/flores
/usr/bin/time -f %U whisper-ctranslate2 15GdH1.mp3  --model medium --device $DEVICE
