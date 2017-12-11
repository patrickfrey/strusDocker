#!/bin/bash

do_build() {
	docker build --no-cache -t patrickfrey/strus-$1 strus-$1 > logs/$1.log 2>&1
	# TEST docker build --no-cache $1 > logs/$1.log 2>&1
}

if [ "$#" -lt 1 ]; then
	(>&2 echo "Usage build.sh image1 image2 ... imageN")
	exit 0
fi

run_build() {
	(do_build $1 && echo "OK" > logs/$1.status) || {
		status=$?
		echo "ERROR" > logs/$1.status
	}
}

mkdir -p logs
for img in $@
do
	run_build $img &
	echo $! > logs/$img.pid
done

jobs=""
for img in $@
do
	jobs+=" $(cat logs/$img.pid)"
done

FAIL=0
for job in $jobs
do
	wait $job || let "FAIL+=1"
done

if [ "$FAIL" == "0" ];
then
	for img in $@
	do
		rm logs/$img.pid
		echo "$img $(cat logs/$img.status)"
	done
	(>&2 echo "done")
	exit 0
else
	(>&2 echo "$FAIL jobs killed")
	exit 1
fi


