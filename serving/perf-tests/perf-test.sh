if ! command -v wrk &> /dev/null
then
    echo "Please install wrk using: 'sudo apt install wrk'"
    exit 1
fi

if [ -z "$1" ]
then
    URL="http://127.0.0.1:8700/translate/"
else
    URL=$1
fi

echo "Doing test on URL:" $URL

echo "** Catalan - English (10 req, 1 at the time)"
wrk -t1 -c1 -d 10s -s post-data-cat-eng.form.lua $URL

echo "** English - Catalan (50 req, 5 at the time)" 
wrk -t10 -c10 -d 10s -s post-data-eng-cat.form.lua $URL

