# Generate final src-val-test single files
head -n 1000000 de-ca-corpus/data/TildeMODEL.de-ca.ca > processed/TildeMODEL.de-ca.ca
head -n 1000000 de-ca-corpus/data/TildeMODEL.de-es.de > processed/TildeMODEL.de-es.de
python3 ../../data-processing-tools/join-single-file.py

