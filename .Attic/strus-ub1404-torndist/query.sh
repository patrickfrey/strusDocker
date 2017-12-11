#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <query>" >&2
    exit 1
fi

query=`echo ${@:2} | sed 's/ /%20/g'`
curl -X GET --data "i=0&n=20&q=$query" http://localhost:80/query


