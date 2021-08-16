currentDate=`date +"%Y-%m-%d"`
filename=eng-cat-$currentDate.zip
zip -r -9 $filename corpus/* 
scp $filename baixades@baixades:/home/baixades/pub/softcatala/opennmt/training-sets/eng-cat/

