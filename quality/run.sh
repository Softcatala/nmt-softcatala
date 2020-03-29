mkdir -p translated
cp ../models/eng-cat/1/assets/*.model .
python3 ../use-models-tools/model-to-txt.py -m eng-cat -f input/common-sentences.en -t translated/common-sentences.ca
diff -u reference/common-sentences.ca translated/common-sentences.ca


