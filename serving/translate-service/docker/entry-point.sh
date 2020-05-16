TARGET=/srv/data/files
mkdir -p $TARGET
# The requests do not requiere CPU since they are waiting from TF, then threads is more appropiated
gunicorn --workers=2 --threads=16 translate-service:app -b 0.0.0.0:8700
