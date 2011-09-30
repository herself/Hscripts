#!/usr/bin/env python
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# A nagios script which checks if you are running out of tapes in a TSM storage pool
# The monitoring machine must have dsmadmc installed
##############

from subprocess import Popen, PIPE
from sys import exit
import re

TRESH = 1
CRIT = 0
CMD = "dsmadmc -id=cluster01 -password=cluster \"select STGPOOL_NAME,NUMSCRATCHUSED,MAXSCRATCH from stgpools\""

prg = Popen(CMD, stdout=PIPE, shell=True)
prg.wait()
prg.poll()
ret = prg.stdout.readlines()

if prg.returncode != 0:
	print ret
	exit(2)

trap = re.compile("(.*?) \s+?(\d+)\s+?(\d+)")
state = 0
out = []

for line in ret:
	m = trap.match(line)
	if m:
		name = m.group(1)
		cur = m.group(2)
		max = m.group(3)
		if int(cur)+TRESH >= int(max):
			state = 1
			out.append("%s tapes: %s/%s" % (name, cur, max))
		elif int(cur)+CRIT >= int(max):
			state = 2
			out.append("CRITICAL: %s tapes: %s/%s" % (name, cur, max))

if state == 0:
	print "Tapes OK"
	exit(0)
else:
	if len(out) > 1:
		print "There are %d tape problems" % (len(out))
	for line in out:
		print line
	exit(state)
