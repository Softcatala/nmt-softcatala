./entry-point.sh &

sleep 20s
cd /srv/api-tst
nosetests
