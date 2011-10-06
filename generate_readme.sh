#!/usr/bin/env zsh
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Generates a README file for the repository :-D
##############

setopt extended_glob
if [[ -f /usr/local/bin/gsed ]]
then
	SED="gsed"
else
	SED="sed"
fi

for i in *~LICENSE~README
do
	echo $i
	echo "---------------------"
	echo $i | egrep -q "\.c$"
	if [[ $? -eq 0 ]]
	then
		cat $i | $SED -n '4,/\/\/ -------------/{s/\/\/ //g;s/\/\///g;s/---//g;p}' | grep -v "XXX"
	else
		cat $i | $SED -n '5,/##############/{s/# //g;s/#//g;p}' | grep -v "XXX"
	fi
done
