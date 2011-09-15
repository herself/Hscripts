#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Shows the status of a given wired interface. Useful for tools like xmobar or dzen
##############

if [[ -z $1 ]] 
then
	echo "I need a interface name given as first argument!"
	exit 1
fi

IP=`ip addr show $1 | grep "inet " | awk '{ print $2 }'`
DOWN=`ip addr show $1 | grep "DOWN"`
CARR=`ip addr show $1| grep "NO-CARRIER"`

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
