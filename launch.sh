#!/usr/bin/env bash
# Author : Brian Robertson (http://msscripting.com/2011/06/12/launch-script/)
# LICENSE unspecified
#
# This is a really handly little script that takes any simple command and runs it in the background. 
# It logs all output into files in ~/.launch in a nice organized manner.
##############

mkdir -p ~/.launch
logfilename="`echo $1 | grep -oe \"[^/]*$\"`_`date +%F_%H:%M:%S,%N`"
echo "== LAUNCH $@ ==" > ~/.launch/${logfilename}_stdout.log
echo "== LAUNCH $@ ==" > ~/.launch/${logfilename}_stderr.log
nohup "$@" >>~/.launch/${logfilename}_stdout.log 2>>~/.launch/${logfilename}_stderr.log &
