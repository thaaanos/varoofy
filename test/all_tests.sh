#!/bin/sh 

# test harness for main programs and features
../version.py > /dev/null
if [ $? ]
then
    echo "Version passed"
else
    echo "Version failed"
fi

# test miner
../miner.py > /dev/null
if [ $? ]
then
    echo "miner passed"
else
    echo "miner failed"
fi

../site.py > /dev/null
if [ $? ]
then
    echo "site passed"
else
    echo "site failed"
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
