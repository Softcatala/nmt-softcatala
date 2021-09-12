#!/bin/bash

git clone https://github.com/Softcatala/parallel-catalan-corpus corpus-raw
cd corpus-raw
git checkout new-corpus

declare -a arr=("eng-cat" "deu-cat" "ita-cat" "fra-cat" "spa-cat" "nld-cat")

for dirname in "${arr[@]}"; do
    echo Copying $dirname
    rm -f -r ../$dirname/corpus-raw/
    mkdir -p ../$dirname/corpus-raw/
    cp -r $dirname/* ../$dirname/corpus-raw/
    pushd .
    cd ../$dirname/corpus-raw/
    if compgen -G "*.xz" > /dev/null; then
         xz -f -d *.xz
    fi
    popd
done


