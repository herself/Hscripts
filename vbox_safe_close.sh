#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Saves the state of all running Virtualbox machines
# I always forget to do that when I halt the system, so aliased halt for
# vbox_safe_close.sh; halt
##############

VM=$(VBoxManage list runningvms)
if [[ -z $VM ]]
then
	echo "No running VMs detected"
	exit
fi

for i in `echo "$VM" | awk '{ print $ 1 }' | sed 's/"//g'`
do
	VBoxManage controlvm $i savestate
done
