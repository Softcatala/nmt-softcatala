
# Translation memories
python3 ../../data-processing-tools/po-to-text.py -f raw/tots-tm.po
mv -f src.txt preprocessed/tots-tm.en
mv -f tgt.txt preprocessed/tots-tm.ca

# Generate final src-val-test single files
python3 ../../data-processing-tools/join-single-file.py
cat src-test1.txt >> src-test.txt
cat tgt-test1.txt >> tgt-test.txt
