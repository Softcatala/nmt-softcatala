VOCSIZE=50000
python3 ../sentencepiece-tokenizer.py -v $VOCSIZE
onmt-build-vocab --size $VOCSIZE --save_vocab src-vocab.txt.token src-train.txt.token
onmt-build-vocab --size $VOCSIZE --save_vocab tgt-vocab.txt.token tgt-train.txt.token
