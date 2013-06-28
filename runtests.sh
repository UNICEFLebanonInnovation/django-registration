#!/bin/bash
# -s (or --nocapture) prevents nose capturing output and thus
# doesn't stymie you when putting in pdb.set_trace() in tests

find . -name '*.pyc' -exec rm {} \;
coverage erase
coverage run runtests.py $* || echo "Test failed"

if [ $? -eq 1 ]
then
    exit 1
fi

# running on the assumption that little goes into most init files
# and having lots of 100% coverage on empty files can skew results
coverage xml
coverage html
pep8 --ignore=W293 -r registration > pep8.txt || echo "PEP-8 violations."
