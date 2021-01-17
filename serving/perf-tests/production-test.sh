URL='https://www.softcatala.org/sc/v2/api/nmt-engcat/translate/'
#URL=http://127.0.0.1:5000/translate/

echo "** Catalan - English (10 req, 1 at the time)"
ab -n 10 -c 1 -p  post-data-cat-eng.form -T application/x-www-form-urlencoded $URL | grep '95%'

echo "** Catalan - English (50 req, 5 at the time)"
ab -n 50 -c 5 -p  post-data-cat-eng.form -T application/x-www-form-urlencoded $URL | grep '95%'

echo "** English - Catalan (10 req, 1 at the time)" 
ab -n 10 -c 1 -p  post-data-eng-cat.form -T application/x-www-form-urlencoded $URL | grep '95%'

echo "** English - Catalan (50 req, 5 at the time)" 
ab -n 50 -c 5 -p  post-data-eng-cat.form -T application/x-www-form-urlencoded $URL | grep '95%'
