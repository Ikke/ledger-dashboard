#!/bin/bash
echo "Press enter to run tests"

while read
do
    nosetests $1 2>&1 | color_test_results
done
