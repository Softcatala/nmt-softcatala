docker volume create traductor-files
docker run -v traductor-files:/srv/data -it --rm -p 8700:8700 translate-service
