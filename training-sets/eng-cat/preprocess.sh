
# Translation memories
python3 ../../data-processing-tools/po-to-text.py -f raw/tots-tm.po
mv -f src.txt preprocessed/tots-tm.en
mv -f tgt.txt preprocessed/tots-tm.ca

# Remove * from Apertium
sed  's/*//g' raw/europarl.en-ca.ca > preprocessed/europarl.en-ca.ca

# Generate Wikimatrix from sources
python3 ../../data-processing-tools/wikimatrix-tsv-to-text.py \
  --tsv raw/WikiMatrix.ca-en.tsv.gz \
  --bitext WikiMatrix.en-ca.txt \
  --src-lang ca --trg-lang en \
  --threshold 1.04

python3 ../../data-processing-tools/clean-wikimatrix.py -s WikiMatrix.en-ca.txt -t preprocessed/WikiMatrix.en-ca.txt
rm WikiMatrix.en-ca.txt.ca
rm WikiMatrix.en-ca.txt.en

# Generate final src-val-test single files
python3 ../../data-processing-tools/join-single-file.py

