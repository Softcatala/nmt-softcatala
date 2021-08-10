# Generate final src-val-test single files
python3 ../../data-processing-tools/join-single-file.py

mkdir -p corpus/deu-cat
cp src-train.txt corpus/deu-cat/src-train.txt
cp src-val.txt corpus/deu-cat/src-val.txt
cp src-test.txt corpus/deu-cat/src-test.txt

# Migrate target language to new grammar rules
python3 ../MTUOC-novaIEC/modificaIEC.py tgt-train.txt corpus/deu-cat/tgt-train.txt
python3 ../MTUOC-novaIEC/modificaIEC.py tgt-val.txt corpus/deu-cat/tgt-val.txt
python3 ../MTUOC-novaIEC/modificaIEC.py tgt-test.txt corpus/deu-cat/tgt-test.txt

# Prepare corpus in subdir
mkdir -p corpus/cat-deu
mv src-train.txt corpus/cat-deu/tgt-train.txt
mv src-val.txt corpus/cat-deu/tgt-val.txt
mv src-test.txt corpus/cat-deu/tgt-test.txt

mv tgt-train.txt corpus/cat-deu/src-train.txt
mv tgt-val.txt corpus/cat-deu/src-val.txt
mv tgt-test.txt corpus/cat-deu/src-test.txt
