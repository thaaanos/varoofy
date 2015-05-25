#!/bin/sh 

PYTHONPATH=$PYTHONPATH:../miner:

# test harness for main programs and features
../version.py > /dev/null
if [ $? ]
then
    echo "Version passed"
else
    echo "Version failed"
fi

../miner.py > /dev/null
if [ $? ]
then
    echo "miner passed"
else
    echo "miner failed"
fi

../miner_site.py > /dev/null
if [ $? ]
then
    echo "miner site passed"
else
    echo "miner site failed"
fi

../miner/collector_database.py > /dev/null
if [ $? ]
then
    echo "collector_database passed"
else
    echo "collector_database failed"
fi

../miner/rss_collector.py > /dev/null
if [ $? ]
then
    echo "rss_collector passed"
else
    echo "rss_collector failed"
fi
