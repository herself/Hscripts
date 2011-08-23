#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Finds the words you can make from the given letters
# XXX: limitations:
# XXX: won't find a word with 3 same letters given (use blank tile instead) 
# XXX: will print some false words, like aaa with given ala
##############

DIR="$HOME/.scrabble" #location of the wordlist
ENCODING="utf-8" #system encoding
URL="http://sjp.pl/slownik/growy/sjp-20110205.tar.gz" #the wordlist archive
#site: http://www.sjp.pl/slownik/growy/

while getopts hs OPT 2> /dev/null; do
	case $OPT in
		"h") echo "usage: $0 [# of blank tiles (default 0)]"
		echo -e "\t-s - downloads the wordlist\n\t-h - this help"
		exit 
		;;
		"s") TMP=`mktemp`
		TMP2=`mktemp`
		echo -n "Downloading..."
		wget $URL -O $TMP &> /dev/null
		echo " done."
		echo -n "Unpacking..."
		zcat $TMP > $TMP2
		echo " done."
		echo -n "Changing file encoding..."
		iconv -f iso-8859-2 -t $ENCODING $TMP2 > $DIR 
		echo " done."
		echo "Sync finished!"
		exit
		;;
	esac
done
if [ -f $DIR ] 
then
	echo "Please input your letters:"
	echo -n "> "
	read REGEX
	LEN=`echo $REGEX | awk '{print length()}'`
	REGEXC=`echo $REGEX | sed ':top;s/\(.*\)\([a-z]\)\(.*\)\2\(.*\)/\1\3\4/;t top'`
	sed "/[$REGEX]\{$LEN\}/!d
	/.*\([$REGEXC]\).*\1/d
	/[a-ząćęłńóśźż]\{$(($LEN+$1+1)),\}/d
	" $DIR
else
	echo "No wordlist found! Use \`$0 -s\` to download one"
fi
