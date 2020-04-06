
# Translation memories memories
#python3 ../../data-processing-tools/po-to-text.py -f raw/tots-tm.po
#mv -f src.txt preprocessed/tots-tm.en
#mv -f tgt.txt preprocessed/tots-tm.ca

# Remove * from Apertium
#sed  's/*//g' raw/europarl.en-ca.ca.raw > preprocessed/europarl.en-ca.ca

#
python3 ../../data-processing-tools/wikimatrix-tsv-to-text.py \
  --tsv raw/WikiMatrix.ca-en.tsv.gz \
  --bitext WikiMatrix.en-ca.txt \
  --src-lang ca --trg-lang en \
  --threshold 1.04

python3 ../../data-processing-tools/clean-wikimatrix.py -s WikiMatrix.en-ca.txt -t preprocessed/WikiMatrix.en-ca.txt
