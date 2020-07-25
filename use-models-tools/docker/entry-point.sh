#!/bin/bash
cd /srv/files
if [ "$FILE_TYPE" = "po" ] ; then
    python3 ../model-to-po.py -p /srv/models/tokenizer/ -x /srv/models/ $COMMAND_LINE
else
    python3 ../model-to-txt.py -p /srv/models/tokenizer/ -x /srv/models/ $COMMAND_LINE
fi
