#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Shows the status of a given wireless interface. Useful for tools like xmobar or dzen
##############

if [[ -z $1 ]] 
then
	echo "I need a interface name given as first argument!"
	exit 1
fi

IP=`iwconfig $1 2> /dev/null | egrep "(ESSID)|(Signal)|(Rate)"|tr -d "\n" | awk '{ printf("%s %s%s %s%s\n", $4, $6, $7, $13, $14)}' | sed 's/ESSID/E/;s/Rate/R/;s/level/L/;s/\/s//;s/"//g;s/=/:/g'`
DOWN=`ip addr show $1 2> /dev/null | grep "DOWN"`
CARR=`ip addr show $1 2> /dev/null | grep "NO-CARRIER"`

if [[ -n $IP ]]
then
	echo "$1: $IP"
else
	if [[ -n $CARR ]]
	then 
		echo "$1: NC" #no carrier
	else
		if [[ -n $DOWN ]]
		then
			echo "$1: DOWN"
		else
			echo "$1: NO CONF?"
		fi
	fi
fi
