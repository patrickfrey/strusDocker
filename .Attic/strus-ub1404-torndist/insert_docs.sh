#!/bin/sh

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <server-port> <start-range> [<end-range>]" >&2
    exit 1
fi

port=`expr 0 \+ $1`
start=`expr 0 \+ $2`
if [ "$#" -lt 3 ]; then
    end=$start
else
    end=`expr 0 \+ $3`
fi
for i in $(seq $start $end)
do
    curl -X POST -d @data/doc/$i.xml localhost:80/insert/$port --header "Content-Type:text/xml"
done

