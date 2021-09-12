#!/bin/bash

#declare -a arr=("ita-cat" "fra-cat" "spa-cat")
declare -a arr=("cat-ita")

for dirname in "${arr[@]}"; do
    echo Processing $dirname

 
    if [ ! -d $dirname ]; then
        mkdir $dirname
    fi

    pushd $dirname

    cp ../master-language/* .
    ./copy-corpus.sh
    ./train.sh
    ./export.sh
    popd
done


