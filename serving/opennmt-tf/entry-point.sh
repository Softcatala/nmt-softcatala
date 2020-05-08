TARGET=/srv/data/models/
mkdir $TARGET
cp /models/eng-cat/1/assets/*.model $TARGET
cp /models/eng-cat/1/assets/model_description.txt  $TARGET/model-description-engcat.txt

cp /models/cat-eng/ models/cat-eng/	$TARGET
cp /models/cat-eng/1/assets/model_description.txt  $TARGET/model-description-cateng.txt

bash
#tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=eng-cat --model_config_file=models.conf 


