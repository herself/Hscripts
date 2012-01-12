#!/bin/bash
ID="cluster01"
PASS="cluster"

RET=`dsmadmc -id=$ID -password=$PASS q path | sed '14,/^$/!d' | grep No | awk '{ printf("Path %s/%s is offline!\n", $1, $3) }'`
if [[ -z $RET ]]
then
	echo "Paths OK"
	exit 0
else
	NUM=`echo "$RET" | wc -l`
	if [[ $NUM -gt 1 ]]
	then
		echo "There are $NUM path problems"
		echo "$RET"
	else
		echo "$RET"
	fi
	exit 2
fi

