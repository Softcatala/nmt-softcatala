TARGET=/srv/data/files
mkdir -p $TARGET
gunicorn translate-service:app -b 0.0.0.0:8700
