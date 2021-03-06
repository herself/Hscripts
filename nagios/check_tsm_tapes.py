#!/usr/bin/env python
# Author : Wieslaw Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# A nagios script which checks if you are running out of tapes in a TSM storage pool
# The monitoring machine must have dsmadmc installed
# XXX: Needs optimalization, badly
##############

from subprocess import Popen, PIPE
from sys import exit
import re

UTIL_TRESH_CRIT = 90
UTIL_TRESH_WARN = 80
CRIT = 0

CMD = "dsmadmc -id=cluster01 -password=cluster \"select STGPOOL_NAME,NUMSCRATCHUSED,MAXSCRATCH from stgpools\""
CMD_PRC = "dsmadmc -id=cluster01 -password=cluster \"select VOLUME_NAME,PCT_UTILIZED,STATUS from volumes where STGPOOL_NAME='_XXX_NAME_'\"| awk '{ if($3 == \"FILLING\"){printf(\"%s \", $2)} } END{printf(\"\\n\")}'"

prg = Popen(CMD, stdout=PIPE, shell=True)
prg.wait()
prg.poll()
ret = prg.stdout.readlines()

if prg.returncode != 0:
	print ret
	exit(2)

trap = re.compile("(.*?) \s+?(\d+)\s+?(\d+)")
num_trap = re.compile("(\d+\.\d+)")

state = 0
out = []

for line in ret:
	m = trap.match(line)
	if m:
		name = m.group(1)
		cur = m.group(2)
		max = m.group(3)

		cmd_prc_fin = re.sub("_XXX_NAME_", name, CMD_PRC)
		prg = Popen(cmd_prc_fin, stdout=PIPE, shell=True)
		prg.wait()
		prg.poll()

		ret = prg.stdout.readline().rstrip("\n")
		num_list = num_trap.findall(ret)
		if len(num_list) != 0:
			all_util = sum([float(x) for x in num_list])/float(len(num_list))
		else:
			continue

		if all_util > UTIL_TRESH_CRIT:
			state = 2
			out.append("CRITICAL: %s tapes: %s/%s (%d filling left, %.1f%% utilzation)" % (name, cur, max, len(num_list), all_util))
		elif all_util > UTIL_TRESH_WARN:
			state = 1
			out.append("%s tapes: %s/%s (%d filling left, %.1f%% utilzation)" % (name, cur, max, len(num_list), all_util))

if state == 0:
	print "Tapes OK"
	exit(0)
else:
	if len(out) > 1:
		print "There are %d tape problems" % (len(out))
	for line in out:
		print line
	exit(state)
