#!/bin/bash
cd /srv/files
if [ "$FILE_TYPE" = "po" ] ; then
    echo python3 ../model-to-po.py -p /srv/models/tokenizer/ -x /srv/models/  $COMMAND_LINE
    python3 ../model-to-po.py -p /srv/models/tokenizer/ -x /srv/models/ $COMMAND_LINE
else
    python3 ../model-to-txt.py -f input.txt -t output.txt -p /srv/models/tokenizer/ -x /srv/models/
fi
sleep 1m
