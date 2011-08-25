#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Opens an xterm window with the program given as an argument. Very nice for binding to a key things like alsamixer or htop, since the second run of the script closes the previously opened window
##############

if [[ -z $1 ]]
then
	echo "An argument is required"
	exit
fi

ps aux | egrep  "[^]eh] ${1}$"
if [[ $? -eq 1 ]]
then
	xterm -geometry 100x20+500+400 -e ${1}
else
	killall ${1}
fi
