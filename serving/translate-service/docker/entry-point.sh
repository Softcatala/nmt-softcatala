UPLOAD_FOLDER=/srv/data/files/
SAVED_TEXTS=/srv/data/saved/
mkdir -p $UPLOAD_FOLDER
mkdir -p $SAVED_TEXTS

# The requests do not requiere CPU since they are waiting from TF, then threads is more appropiated
gunicorn --workers=2 --graceful-timeout 90 --timeout 90 --threads=16 translate-service:app -b 0.0.0.0:8700
