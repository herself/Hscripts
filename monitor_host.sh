#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Monitors a host and plays a sound when the given port comes online
##############

WAV="/usr/share/skype/sounds/ContactAuthRequest.wav"
TRY="1"
HOST=$1
PORT=$2

if [[ (-z $HOST) || (-z $PORT) ]]
then
	echo "Usage: $0 [host] [port]"
	exit
fi

while true 
do
	echo -n "$HOST:$PORT -> try #${TRY} @ "
	date
	nmap -sT $HOST -p $PORT | grep -A 1 PORT | sed '1d' | grep "open" > /dev/null
	if [[ $? -eq 0 ]]
	then
		mplayer -quiet $WAV > /dev/null 2>&1 
		break
	fi
	TRY=`echo "${TRY}+1" | bc`
	sleep 1
done
