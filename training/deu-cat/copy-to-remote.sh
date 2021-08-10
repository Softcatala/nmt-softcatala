rm -f train-test-val.zip
zip -r train-test-val.zip corpus/
scp -i ~/.ssh/london-pair.pem  train-test-val.zip ${NMT_MACHINE}:/home/ubuntu/nmt-softcatala/training/deu-cat


