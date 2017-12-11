#!/bin/bash

do_test() {
	docker run -t -i patrickfrey/$1 /test.sh >> logs/$1.test.log 2>&1
}

if [ "$#" -lt 1 ]; then
	(>&2 echo "Usage test.sh image1 image2 ... imageN")
	exit 0
fi

run_test() {
	(do_test $1 && echo "OK" > logs/$1.test.status) || {
		status=$?
		echo "ERROR" > logs/$1.test.status
	}
}

mkdir -p logs
for img in $@
do
	run_test $img &
	echo $! > logs/$img.test.pid
done

jobs=""
for img in $@
do
	jobs+=" $(cat logs/$img.test.pid)"
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
		rm logs/$img.test.pid
		echo "$img $(cat logs/$img.test.status)"
	done
	(>&2 echo "done")
	exit 0
else
	(>&2 echo "$FAIL jobs killed")
	exit 1
fi

