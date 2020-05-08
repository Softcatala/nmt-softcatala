gunicorn translate-service:app -b 0.0.0.0:8700 &
python3 process-batch.py &
tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=eng-cat --model_config_file=models.conf 


