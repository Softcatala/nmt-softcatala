modelName=${PWD##*/}
rm exported/ -r -f
mkdir -p exported/metadata
mkdir -p exported/tokenizer

source bleu.sh

modelDescription="exported/metadata/model_description.txt"
currentDate=`date +"%Y-%m-%d-%s"`
#read -p 'Describe model: ' uservar
onmt-main --config data.yml --auto_config export --export_dir exported/tensorflow/
echo "Model description: $modelName" >> $modelDescription
cat bleu.txt >>  $modelDescription
echo "Date: $currentDate" >> $modelDescription
python3 ../stack-versions.py >> $modelDescription
wc src-train.txt -l > exported/metadata/inputs_used.txt
ls *.txt -l >> exported/metadata/inputs_used.txt
cp *.model exported/tokenizer/
cp data.yml exported/metadata/
cp sp-vocab.txt.token exported/tensorflow/assets/
ct2-opennmt-tf-converter --model_path run/ --model_type TransformerBaseRelative --output_dir exported/ctranslate2 --src_vocab sp-vocab.txt.token --tgt_vocab sp-vocab.txt.token --quantization int8
cd exported && zip -r ../$modelName-$currentDate.zip *
