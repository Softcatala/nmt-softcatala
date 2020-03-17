gunicorn translate-service:app -b 0.0.0.0:8700 &
tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=eng-cat --model_base_path=/models/eng-cat

