./entry-point.sh &
while ! httping -qc1 http://localhost:8700 ; do sleep 1 ; echo "Waiting for server to respond"; done
cd /srv/api-tst
nose2
