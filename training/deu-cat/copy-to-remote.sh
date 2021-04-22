rm -f train-test-val.zip
zip train-test-val.zip *train*.txt *val*.txt *test*.txt
scp -i ~/.ssh/london-pair.pem  train-test-val.zip ${NMT_MACHINE}:/home/ubuntu/nmt-softcatala/training/deu-cat


