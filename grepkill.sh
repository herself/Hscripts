#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Shows a list of processes which match the given pattern and
# then allows you to kill it
##############

if [[ -z $1 ]] 
then
	echo "I need a pattern to look for kind sir!"
	exit 1
fi

FILE=`mktemp /tmp/ps.XXXXXXXXXXXXXXXXXXXXXXXX`
ps ax -O login > $FILE
cat $FILE | grep -v "grepkill" | grep -i $1 | gawk 'BEGIN{i=1}{printf("%d) %s\n", i, $0); i++}'
echo "Which process to kill?"
read DIEDIE 
kill `cat $FILE | grep -v "grepkill" | grep $1 | sed -n "${DIEDIE}p" | gawk '{ print $1 }'`
rm $FILE
