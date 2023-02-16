#!/bin/bash
cd /srv/files
if [ "$FILE_TYPE" = "po" ] ; then
    model_to_po -x /srv/models/ $COMMAND_LINE
else
    model_to_txt -x /srv/models/ $COMMAND_LINE
fi
