echo "** Catalan - English (10 req, 1 at the time)"
ab -n 10 -c 1 -p  post-data-cat-eng.json -T application/json https://www.softcatala.org/sc/v2/api/nmt-engcat/translate/ | grep '95%'

echo "** Catalan - English (50 req, 5 at the time)"
ab -n 50 -c 5 -p  post-data-cat-eng.json -T application/json https://www.softcatala.org/sc/v2/api/nmt-engcat/translate/ | grep '95%'

echo "** English - Catalan (10 req, 1 at the time)" 
ab -n 10 -c 1 -p  post-data-eng-cat.json -T application/json https://www.softcatala.org/sc/v2/api/nmt-engcat/translate/ | grep '95%'

echo "** English - Catalan (50 req, 5 at the time)" 
ab -n 50 -c 5 -p  post-data-eng-cat.json -T application/json https://www.softcatala.org/sc/v2/api/nmt-engcat/translate/ | grep '95%'


