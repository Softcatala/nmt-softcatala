#!/bin/bash
if [ "$FILE_TYPE" = "po" ] ; then
    cat > input.po
    python3 model-to-po.py -f input.po  -p /srv/models/tokenizer/ -x /srv/models/ >/dev/null
    cat input.po-ca.po
else
    cat > input.txt
    python3 model-to-txt.py -f input.txt -t output.txt -p /srv/models/tokenizer/ -x /srv/models/ >/dev/null
    cat output.txt
fi


