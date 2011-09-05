#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Takes a screenshot of a selected area and then displays it - useful for making fast memos, for example for interface configuration before changing it
##############

SCRDIR="$HOME/Scr/"
mkdir -p "$SCRDIR"

ps aux | grep -v grep | grep unclutter &> /dev/null
UNC_RUNNING=$?

if [[ $UNC_RUNNING -eq 0 ]]
then
	killall unclutter
fi

sleep 0.3s
scrot -s '%Y-%m-%d_$wx$h.png' -e "mv \$f $SCRDIR && feh $SCRDIR/\$f" 

if [[ $UNC_RUNNING -eq 0 ]]
then
	unclutter -visible -grab&
fi
