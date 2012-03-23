#!/usr/bin/env bash
# Author : Shamelesly copied from http://stackoverflow.com/questions/1657232/how-can-i-calculate-an-md5-checksum-of-a-directory
# LICENSE unspecified
#
# Produces a md5 checksum on a given directory. Very handy to check
# if directories differ
##############

if [[ -z $1 ]] 
then
	echo "I need a directory to hash kind sir!"
	exit 1
fi

find $1 -type f -exec md5sum {} + | awk '{print $1}' | sort | md5sum
