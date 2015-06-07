#!/bin/sh 

PYTHONPATH=$PYTHONPATH:../miner:

if [ "$1" == "-d" ]
then
    echo "debug"
    debug="/dev/stdout"
else
    debug="/dev/null"
fi

# test harness for main programs and features
echo "* version test:"
../version.py > "$debug"
if [ $? ]
then
    echo "Version passed"
else
    echo "Version failed"
fi

echo "* miner.py test:"
../miner/mine.py > "$debug"
if [ $? ]
then
    echo "mine passed"
else
    echo "mine failed"
fi

echo "* mine_site.py test:"
../miner/mine_site.py > "$debug"
if [ $? ]
then
    echo "mine_site passed"
else
    echo "mine_site failed"
fi

echo "* collector_database test:"
../miner/collector_database.py > "$debug"
if [ $? ]
then
    echo "collector_database passed"
else
    echo "collector_database failed"
fi

echo "* rss_collector.py test:"
../miner/rss_collector.py > "$debug"
if [ $? ]
then
    echo "rss_collector passed"
else
    echo "rss_collector failed"
fi
