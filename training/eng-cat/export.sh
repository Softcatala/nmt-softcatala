rm -f exported.zip
rm exported/ -r -f
mkdir -p exported/metadata
mkdir -p exported/tokenizer

modelDescription="exported/metadata/model_description.txt"
currentDate=`date +"%Y-%m-%d-%s"`
read -p 'Describe model: ' uservar
onmt-main --config data.yml --auto_config export --export_dir exported/tensorflow/
echo "Model description: $uservar" >  $modelDescription
cat bleu.txt >>  $modelDescription
echo "Date: $currentDate" >> $modelDescription
ls *.txt -l > exported/metadata/inputs_used.txt
cp *.model exported/tokenizer/
cp data.yml exported/metadata/
cp src-vocab.txt.token exported/tensorflow/assets/
cp tgt-vocab.txt.token exported/tensorflow/assets/
onmt-main --config data.yml --auto_config export --export_dir exported/ctranslate2 --export_format ctranslate2
cd exported && zip -r ../exported-$currentDate.zip *
