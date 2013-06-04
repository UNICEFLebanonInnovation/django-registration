#!/bin/bash
# -s (or --nocapture) prevents nose capturing output and thus
# doesn't stymie you when putting in pdb.set_trace() in tests

find . -name '*.pyc' -exec rm {} \;
coverage run runtests.py $*

if [ $? -eq 1 ]
then
    exit 1
fi

# running on the assumption that little goes into most init files
# and having lots of 100% coverage on empty files can skew results
coverage html --omit="settings.py","test_settings.py"

# try to open the page in chrome, but if not present, don't complain
which google-chrome
if [ $? -eq 0 ]
then
  google-chrome htmlcov/index.html
else
  echo "Please see coverage report in file://$PWD/htmlcov/index.html"
fi

cd ..