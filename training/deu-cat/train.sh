#--num_gpus 4 for -> multiple gpus
onmt-main --mixed_precision --model_type TransformerRelative --config data.yml --auto_config train --with_eval
