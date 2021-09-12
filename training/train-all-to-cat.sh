#!/bin/bash

#declare -a arr=("ita-cat" "fra-cat" "spa-cat")
declare -a arr=("fra-cat")

for dirname in "${arr[@]}"; do
    echo Processing $dirname
    pushd $dirname
    ./preprocess.sh
    ./voc.sh
    ./train.sh
    ./export.sh
    popd
done


