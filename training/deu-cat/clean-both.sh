pushd clean-both
head ccaligned.en -n 1000 > ccaligned.2000.en
tail ccaligned.en -n 1000 >> ccaligned.2000.en
head ccaligned.ca -n 1000 > ccaligned.2000.ca
tail ccaligned.ca -n 1000 >> ccaligned.2000.ca
python3 ../../../data-processing-tools/clean-both.py -s ccaligned.2000 -t ccaligned-clean
popd
