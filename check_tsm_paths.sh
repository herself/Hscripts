#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# A nagios script which checks if all TSM paths are online
# The monitoring machine must have dsmadmc installed
##############

ID="cluster01"
PASS="cluster"

RET=`dsmadmc -id=$ID -password=$PASS q path | sed '14,/^$/!d' | grep No | awk '{ printf("Path %s/%s is offline!\n", $1, $3) }'`
if [[ -z $RET ]]
then
	echo "Paths OK"
	exit 0
else
	echo -e $RET
	exit 2
fi

