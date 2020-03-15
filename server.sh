docker run -t --rm -p 8501:8501 -p 8500:8500 \
    -v "$PWD/models/model-sc:/models/model-sc" \
    -e MODEL_NAME=model-sc \
    opennmt/tensorflow-serving:2.1.0  --enable_batching=true

