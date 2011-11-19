#!/usr/bin/env python
# Author : Wieslaw Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Update you mercurial repos with a single script
# Uses python3 and the locate tool
##############

from subprocess import Popen, PIPE
from sys import stdin
from os import getenv
from time import sleep
import re

def run_cmd(command):
	prg = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
	prg.wait()
	prg.poll()
	ret = prg.stdout.readlines()
	return [x.decode("utf-8") for x in ret]

OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

#this is a file with the directories to get excluded
#one directory per line, full paths, no variables
EXCLUDES = "{}/.syncer_exclude".format(getenv("HOME"))
EXCLUDE_PATTERN_CMD = "cat {}".format(EXCLUDES)
FIND_HG_REPOS_CMD = "locate \".hg/hgrc\""

try:
	with open(EXCLUDES, "r") as f:
		EXCLUDES = [x.rstrip("\n") for x in f.readlines()]
except IOError:
	EXCLUDES = []

hg_repos = [re.sub(".hg/hgrc", "", line).rstrip("\n") for line in run_cmd(FIND_HG_REPOS_CMD)]
#excude EXCLUDES
hg_repos = [x for x in hg_repos if sum([1 for y in EXCLUDES if x.startswith(y)]) == 0]

print("Found {} repos (after applying {} exclusion rules), running checks...".format(len(hg_repos), len(EXCLUDES)))

results = {}
#try:
#  import concurrent.futures
#  commands = ["cd {} && hg in".format(x) for x in hg_repos]
#  with concurrent.futures.ProcessPoolExecutor(max_workers=30) as executor:
#    for (x, y) in zip(hg_repos, executor.map(run_cmd, commands)):
#      results[x] = y
#in python versions before 3.2 and in systems that don't support concurrent.futures we use
#run the commands manually (and also in paralell)
#except (NotImplementedError, ImportError):
#the above sucks, it's not even considerably faster...

prgs = {}
for repo in hg_repos:
	prgs[repo] = (Popen("cd {} && hg in".format(repo), stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True), Popen("cd {} && hg out".format(repo), stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True))
	sleep(0.2)
for k, (inb, out) in prgs.items():
	inb.wait()
	out.wait()
	results[k] = ([x.decode("utf-8") for x in inb.stdout.readlines()], [x.decode("utf-8") for x in out.stdout.readlines()])

out_update = []
in_update = []
print("Summary:")
for k, (inb, out) in results.items():
	print("`--> {}".format(k), end="")

	if inb == []:
		in_result = "{}auth-error?{}".format(WARNING, ENDC)
	elif "no changes found\n" in inb:
		in_result = "{}inbound up to date{}".format(OKGREEN, ENDC)
	else:
		num_changes = sum([1 for x in inb if x.startswith("date: ")])
		in_result = "{}{} inbound changes {}".format(FAIL, num_changes, ENDC)
		in_update.append(k)

	if "no changes found\n" in out:
		out_result = "{}outbound up to date{}".format(OKBLUE, ENDC)
	else:
		num_changes = sum([1 for x in out if x.startswith("date: ")])
		if num_changes > 0:
			out_result = "{}{} outbound changes{}".format(FAIL, num_changes, ENDC)
			out_update.append(k)
		else:
			if len(out) == 1:
				out_result = "{}auth-error?{}".format(WARNING, ENDC)
			else:
				out_result = "UNKNOWN - please test output"

	print(": {} / {}".format(in_result, out_result))

try:
	if in_update == [] and out_update == []:
		print("Noting to update!")
	else:
		if in_update != []:
			print("Perform inbound updates? (y/N)")
			char = stdin.read(1)
			if char == "y" or char == "Y":
				for repo in in_update:
					cmd ="cd {} && hg pull -u".format(repo) 
					print("{}{}{}".format(OKGREEN, cmd, ENDC))
					prg = Popen(cmd, shell=True)
					prg.wait()
			else:
				raise KeyboardInterrupt
		if out_update != []:
			print("Perform outbound updates? (y/N)")
			char = stdin.read(1)
			if char == "y" or char == "Y":
				for repo in out_update:
					cmd ="cd {} && hg push".format(repo) 
					print("{}{}{}".format(OKGREEN, cmd, ENDC))
					prg = Popen(cmd, shell=True)
					prg.wait()
			else:
				raise KeyboardInterrupt
except KeyboardInterrupt:
	print("\nOkay, bye!")
