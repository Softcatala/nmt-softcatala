
# Translation memories
python3 ../../data-processing-tools/po-to-text.py -f raw/tots-tm.po
mv -f src.txt preprocessed/tots-tm.en
mv -f tgt.txt preprocessed/tots-tm.ca

# Generate final src-val-test single files
cat src-test1.txt >> preprocessed/tots-tm.en
cat tgt-test1.txt >> preprocessed/tots-tm.ca
python3 ../../data-processing-tools/join-single-file.py

