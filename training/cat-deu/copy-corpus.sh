# Copy from eng-cat and invert order
cp ../deu-cat/src-train.txt.token tgt-train.txt.token
cp ../deu-cat/src-val.txt.token tgt-val.txt.token
cp ../deu-cat/src-vocab.txt.token tgt-vocab.txt.token
cp ../deu-cat/src-test.txt.token tgt-test.txt.token
cp ../deu-cat/tgt-train.txt.token src-train.txt.token
cp ../deu-cat/tgt-val.txt.token src-val.txt.token
cp ../deu-cat/tgt-vocab.txt.token src-vocab.txt.token
cp ../deu-cat/tgt-test.txt.token src-test.txt.token
cp ../deu-cat/src-test.txt tgt-test.txt
cp ../deu-cat/ca_m.model .
cp ../deu-cat/en_m.model .
 


