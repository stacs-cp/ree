#!/bin/sh
# hardcode EssenceCatalog spec upper bounds as 100 when not given
find problems -name \*.essence -print > a.txt
fgrep -l '..)' `cat a.txt` > b.txt
perl -pi -e 's/\.\.\)/..100)/g' `cat b.txt`
