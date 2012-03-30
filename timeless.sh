#!/usr/bin/env sh
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Shows all given files in a given directory by modification time. Useful for folders with a ton of logs in them
##############

for i in $(ls -t); do 
	echo $(ls -l $i)
	read
	more $i
done
