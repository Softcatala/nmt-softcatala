# Copy from eng-cat and invert order
cp ../eng-cat/src-train.txt.token tgt-train.txt.token
cp ../eng-cat/src-val.txt.token tgt-val.txt.token
cp ../eng-cat/src-vocab.txt.token tgt-vocab.txt.token
cp ../eng-cat/src-test.txt.token tgt-test.txt.token
cp ../eng-cat/tgt-train.txt.token src-train.txt.token
cp ../eng-cat/tgt-val.txt.token src-val.txt.token
cp ../eng-cat/tgt-vocab.txt.token src-vocab.txt.token
cp ../eng-cat/tgt-test.txt.token src-test.txt.token
cp ../eng-cat/src-test.txt tgt-test.txt
cp ../eng-cat/ca_m.model .
cp ../eng-cat/en_m.model .
 


