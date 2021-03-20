rm -f exported.zip
rm exported/ -r -f
mkdir -p exported/metadata
mkdir -p exported/tokenizer

if [ ! -f bleu.txt ]; then
    source bleu.sh
fi

modelDescription="exported/metadata/model_description.txt"
currentDate=`date +"%Y-%m-%d-%s"`
read -p 'Describe model: ' uservar
onmt-main --config data.yml --auto_config export --export_dir exported/tensorflow/
echo "Model description: $uservar" >  $modelDescription
cat bleu.txt >>  $modelDescription
echo "Date: $currentDate" >> $modelDescription
python3 ../stack-versions.py >> $modelDescription
ls *.txt -l > exported/metadata/inputs_used.txt
cp *.model exported/tokenizer/
cp data.yml exported/metadata/
cp src-vocab.txt.token exported/tensorflow/assets/
cp tgt-vocab.txt.token exported/tensorflow/assets/
#onmt-main --config data.yml --auto_config export --export_dir exported/ctranslate2 --export_format ctranslate2
ct2-opennmt-tf-converter --model_path run/ --model_spec TransformerBaseRelative --output_dir exported/ctranslate2 --src_vocab src-vocab.txt.token --tgt_vocab tgt-vocab.txt.token --quantization int8
cd exported && zip -r ../exported-$currentDate.zip *
