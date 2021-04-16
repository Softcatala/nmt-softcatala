onmt-main --config data.yml --auto_config infer --features_file src-test.txt.token > predictions.txt.token
perl ../multi-bleu.perl tgt-test.txt.token < predictions.txt.token 
python3 ../sentencepiece-bleu.py
perl ../multi-bleu.perl tgt-test.txt < predictions.txt > bleu.txt
cat bleu.txt
