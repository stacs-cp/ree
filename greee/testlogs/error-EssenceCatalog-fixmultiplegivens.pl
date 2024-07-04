#!/bin/sh
# turn "given a, b : t" into "given a : t" and "given b : t"
# CAVEATS:
# hardcodes end-of-line as LF even if file uses CR-LF convention
# pattern matches comments containing given and a comma, hardcode an exception
# doesn't match multiline givens or "given a : t1, b : t2"
grep -l 'given [^:\$]*,[^:]*:[^:]*$' `cat a.txt` | fgrep -v 'Ramsey' > c.txt
perl -pi -e '1 while s/given ([^:\$]*), *([^:\$,]*)(:.*)/given \1\3\ngiven \2\3/g' `cat c.txt`

