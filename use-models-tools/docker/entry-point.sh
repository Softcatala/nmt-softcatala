#!/bin/bash
cd /srv/files
if [ "$FILE_TYPE" = "po" ] ; then
    python3 ../model-to-po.py -x /srv/models/ $COMMAND_LINE
else
    python3 ../model-to-txt.py -x /srv/models/ $COMMAND_LINE
fi
