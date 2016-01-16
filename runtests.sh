#!/bin/bash

if [[ $1 == "-c" ]]
then
    shift
    while [[ $? -eq 0 ]]
    do
        nosetests $@ 2>&1 | utils/color_test_results

        echo "Press enter to run tests"

        read
    done
else
    nosetests $@ 2>&1 | utils/color_test_results
fi

