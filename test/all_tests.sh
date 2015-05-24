#!/bin/sh 

# test harness for main programs and features
../version.py > /dev/null
if [ $? ]
then
    echo "Version passed"
else
    echo "Version failed"
fi
