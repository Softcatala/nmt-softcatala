srcModelName=${PWD##*/}
VOCSIZE=50000
cp corpus/$srcModelName/*.txt .
python3 ../sentencepiece-tokenizer.py -v $VOCSIZE -l $srcModelName
onmt-build-vocab --from_vocab sp_m.vocab --from_format sentencepiece --save_vocab sp-vocab.txt.token

