./entry-point.sh &

sleep 30s
cd /srv/api-tst
nosetests
