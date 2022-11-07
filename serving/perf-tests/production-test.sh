URL='https://www.softcatala.org/sc/v2/api/nmt-engcat/translate/'
#URL=http://127.0.0.1:5000/translate/

echo "** Catalan - English (10 req, 1 at the time)"
wrk -t1 -c1 -d 10s -s post-data-cat-eng.form.lua $URL

echo "** English - Catalan (50 req, 5 at the time)" 
wrk -t10 -c10 -d 10s -s post-data-eng-cat.form.lua $URL

