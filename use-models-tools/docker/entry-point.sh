#!/bin/bash

COMMAND_LINE="-f flores200.eng -t output.cat -m eng-cat"

cd /srv/flores
if [ "$FILE_TYPE" = "po" ] ; then
    model_to_po -x /srv/models/ $COMMAND_LINE
else
    model_to_txt -x /srv/models/ $COMMAND_LINE
fi
