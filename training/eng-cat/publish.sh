rm -f eng-cat.zip
zip -r -9 eng-cat.zip raw/* *.txt preprocessed/*
scp *.zip  baixades@baixades:/home/baixades/pub/softcatala/opennmt/training-sets/eng-cat/

