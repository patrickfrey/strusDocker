#!/bin/sh

#ps -fe | grep python | grep strus | awk '{print $2}' | xargs kill -s SIGTERM
./strusStatisticsServer.py -p 7100 &
sleep 3
./strusStorageServer.py -s 7100 -p 7101 -c path=storage -P &
./strusHttpServer.py -p 8081 7101 &

. ./insert_docs_8081.sh 7101 0 33



