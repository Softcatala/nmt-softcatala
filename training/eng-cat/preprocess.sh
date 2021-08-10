
# Translation memories
python3 ../../data-processing-tools/po-to-text.py -f raw/tots-tm.po
mv -f src.txt preprocessed/tots-tm.en
mv -f tgt.txt preprocessed/tots-tm.ca

# Generate final src-val-test single files
python3 ../../data-processing-tools/join-single-file.py

mkdir -p corpus/eng-cat
cp src-train.txt corpus/eng-cat/src-train.txt
cp src-val.txt corpus/eng-cat/src-val.txt
cp src-test.txt corpus/eng-cat/src-test.txt

# Migrate target language to new grammar rules
python3 ../MTUOC-novaIEC/modificaIEC.py tgt-train.txt corpus/eng-cat/tgt-train.txt
python3 ../MTUOC-novaIEC/modificaIEC.py tgt-val.txt corpus/eng-cat/tgt-val.txt
python3 ../MTUOC-novaIEC/modificaIEC.py tgt-test.txt corpus/eng-cat/tgt-test.txt

# Prepare corpus in subdir
mkdir -p corpus/cat-eng
mv src-train.txt corpus/cat-eng/tgt-train.txt
mv src-val.txt corpus/cat-eng/tgt-val.txt
mv src-test.txt corpus/cat-eng/tgt-test.txt

mv tgt-train.txt corpus/cat-eng/src-train.txt
mv tgt-val.txt corpus/cat-eng/src-val.txt
mv tgt-test.txt corpus/cat-eng/src-test.txt
