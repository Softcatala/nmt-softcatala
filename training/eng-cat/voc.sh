VOCSIZE=50000
python3 ../sentencepiece-tokenizer.py -v $VOCSIZE
onmt-build-vocab --from_vocab en_m.model.vocab --save_vocab src-vocab.txt.token
onmt-build-vocab --from_vocab en_m.model.vocab --save_vocab tgt-vocab.txt.token
