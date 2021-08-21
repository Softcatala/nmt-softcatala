id=$(docker create nmt-models)
echo id:$id
sudo docker cp $id:/srv/models/.  /srv/models/
docker rm -v $id
