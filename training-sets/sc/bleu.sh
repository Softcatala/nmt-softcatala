onmt-main --config data.yml --auto_config infer --features_file src-test.txt > predictions.txt
perl ../OpenNMT-py/tools/multi-bleu.perl tgt-test.txt < predictions.txt 

