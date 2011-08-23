#!/usr/bin/env zsh
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Generates a README file for the repository :-D
##############

setopt extended_glob

for i in *~LICENSE~README
do
	echo $i
	echo "---------------------"
	cat $i | sed -n '5,/##############/{s/# //g;s/#//g;p}' | grep -v "XXX"
done
