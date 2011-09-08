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
LIST=`mktemp /tmp/ps.XXXXXXXXXXXXXXXXXXXXXXXX`
ps ax -O login > $FILE
cat $FILE | grep -v "grepkill" | grep -i $1 | gawk 'BEGIN{i=1}{printf("%d) %s\n", i, $0); i++}' > $LIST
if [ `cat $LIST | wc -l` == 0 ]
then
	echo "No processes found!"
	exit 1
fi

cat $LIST
echo "Which process to kill? (please give a number, numbers separated by spaces, or a range. example: 1-10 13 14 16-17)"
read DIEDIE 
DIEDIE=`echo "$DIEDIE" | perl -pe 's/(\d+)-(\d+)/{$1..$2}/g'`
for NUM in `eval echo "$DIEDIE"`
do
	DEADPID=`cat $FILE | grep -v "grepkill" | grep $1 | sed -n "${NUM}p" | gawk '{ print $1 }'`
	kill -9 $DEADPID
	echo "Killed $DEADPID"
done

rm $FILE $LIST
