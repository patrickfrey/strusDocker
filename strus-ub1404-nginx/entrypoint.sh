#!/bin/bash
set -e

# -- parse argument string and extract some known options:
arg=$@
storage=""
while [[ $# > 0 ]]
do
key="$1"
case $key in
	-s|--storage)
	storage="$2"
	shift
	;;
	*)
	shift
	;;
esac
done

# -- start required services:
service php5-fpm start
service nginx start

# -- command handler:
case "$arg[0]" in
	strusRpcServer*)
		if [[ -d "$storage" ]]
		then echo "Storage $storage exists"
		else
			strusCreate -s "path=$storage";
		fi
		exec "$arg"
	;;
	*)
		exec "$arg"
	;;
esac

