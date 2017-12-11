#!/bin/sh

#ps -fe | grep python | grep strus | awk '{print $2}' | xargs kill -s SIGTERM
rm -Rf storage7184
rm -Rf storage7185
rm -Rf storage7186

strusCreate -s "path=storage7184; metadata=doclen UINT16, date UINT32"
strusCreate -s "path=storage7185; metadata=doclen UINT16, date UINT32"
strusCreate -s "path=storage7186; metadata=doclen UINT16, date UINT32"

./strusStatisticsServer.py -p 7183 &
sleep 3
./strusStorageServer.py -p 7184 -c path=storage7184 -P &
./strusStorageServer.py -p 7185 -c path=storage7185 -P &
./strusStorageServer.py -p 7186 -c path=storage7186 -P &
./strusHttpServer.py -p 8080 7184 7185 7186 &

. ./insert_docs_8080.sh 7184 0
. ./insert_docs_8080.sh 7185 1 2
. ./insert_docs_8080.sh 7186 3 33



