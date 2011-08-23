#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Displays a random fortune from bash.org.pl 
# Only in polish, sorry!
##############

while getopts hs OPT 2> /dev/null; do
	case $OPT in
		"h") echo -e "Pomoc:\n\t-s - synchronizuje baze cytatów\n\t-h - ta pomoc"
		exit 
		;;
		"s") wget http://bash.org.pl/text -O ~/.fortunki
		exit
		;;
	esac
done
if [ -f ~/.fortunki ] 
then
	tail -n $(($RANDOM%`cat ~/.fortunki | wc -l`)) ~/.fortunki | 
	gsed -n '/^#/,/^%/{
					/^%/q
					s/<[bB][rR]>//g
					s/&nbsp;//g
					/^$/d
					/^#/!p}'
else
	echo "Brak pliku z fortunkami! Uzyj \`$0 -s\` by sciagnac baze fortunek"
fi
