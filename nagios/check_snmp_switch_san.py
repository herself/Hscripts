#!/usr/bin/env python
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# A nagios script which checks the status of sensors and ports on a BROCADE FC switch
# XXX: The port status is a bit bugged, as the ConnectorPresent snmp value checks the presence of a GBIC adapter, not a fibre cable
#
# Based on a really ugly (yet educational) script by Roderick Derks (roderick@r71.nl)
##############

from optparse import OptionParser
from subprocess import Popen, PIPE
from sys import stdout
import re

SNMP_SENSORS = "SNMPv2-SMI::enterprises.1588.2.1.1.1.1.22.1"
SNMP_TYPE = "SNMPv2-SMI::mib-2.47.1.1.1.1.2.1"
SNMP_IF = { "name": "IF-MIB::ifDescr", "admin": "IF-MIB::ifAdminStatus", "oper": "IF-MIB::ifOperStatus", "connect": "IF-MIB::ifConnectorPresent", "data": "IF-MIB::ifOutOctets"};

STATE_OK = 0;
STATE_WARNING = 1;
STATE_CRITICAL = 2;
STATE_UNKNOWN = 3;

def gb(name):
	return re.search(".*\((\d)\).*", name).group(1)

def check_sensor(name, nice_name, plot_name, host, community):
	retcode = STATE_OK
	r_obj = re.compile("%s\.\d\.(.*?) .*%s" % (SNMP_SENSORS, name))

	snmp_info = Popen("snmpbulkwalk -v 2c -c %s %s %s" % (community, host, SNMP_SENSORS), stdout=PIPE, shell=True).stdout.readlines()
	indexes = [r_obj.match(line).group(1) for line in snmp_info if r_obj.match(line)]

	r_obj_rel = re.compile("%s\.3\.(%s).*: (\d+)" % (SNMP_SENSORS, "|".join(indexes)))
	r_obj_sen = re.compile("%s\.4\.(%s).*: (\d+)" % (SNMP_SENSORS, "|".join(indexes)))
	rel = [r_obj_rel.match(line).group(2) for line in snmp_info if r_obj_rel.match(line)]
	sen = [r_obj_sen.match(line).group(2) for line in snmp_info if r_obj_sen.match(line)]
	if sum([1 for x in rel if int(x) == 4]) == len(rel):
		stdout.write("%s HEALTHY" % (nice_name))
	else:
		stdout.write("%s CRITICAL" % (nice_name))
		retcode = STATE_CRITICAL
	if plot_name:
		stdout.write("|")
		for (i, temp) in enumerate(sen):
			stdout.write("%s%d_t=%s " % (plot_name, i+1, temp))
	stdout.write("\n")
	return retcode

def check_type(host, community):
	snmp_info = Popen("snmpbulkwalk -v 2c -c %s %s %s" % (community, host, SNMP_TYPE), stdout=PIPE, shell=True).stdout.readline()
	print re.search("\"(.*)\"", snmp_info).group(1)
	return STATE_OK

def check_fc_ports(host, community):
	snmp_info = {}
	if_map = {}
	problems = []
	problems_if = []
	r_name = re.compile(".*?(\d+).*FC.*(\d+/\d+)")
	r_other = re.compile(".*?(\d+).* (.*)")
	for (k, v) in SNMP_IF.items():
		snmp_info[k] = Popen("snmpbulkwalk -v 2c -c %s %s %s" % (community, host, v), stdout=PIPE, shell=True).stdout.readlines()
		if k == "name":
			if_map[k]= dict([r_name.match(line).groups() for line in snmp_info[k] if r_name.match(line)])
		else: 
			if_map[k] = dict([r_other.match(line).groups() for line in snmp_info[k] if r_other.match(line)])
	for (k, v) in sorted(if_map["name"].items()):
		if ((gb(if_map["admin"][k]) != gb(if_map["oper"][k])) or (gb(if_map["oper"][k]) != gb(if_map["connect"][k]))) and (int(if_map["data"][k]) > 0):
			problems_if.append(v)
			problems.append("problem on: %s (admin: %s, oper: %s, cable: %s, dataOut: %s)!" % (v, if_map["admin"][k], if_map["oper"][k], if_map["connect"][k], if_map["data"][k]))
	if problems:
		print "FC port problem: %s" % (" ".join(problems_if))
		print "extended info:"
		for line in problems:
			print line
		return STATE_CRITICAL
	else:
		print "fc ports ok"
		return STATE_OK

parser = OptionParser()
parser.add_option("-n", "--type", action="store_true", dest="type", default=False, help="Print the machine type")
parser.add_option("-t", "--temp", action="store_true", dest="temp", default=False, help="Print the temperature stats")
parser.add_option("-f", "--fan", action="store_true", dest="fan", default=False, help="Print the fan stats")
parser.add_option("-p", "--psu", action="store_true", dest="psu", default=False, help="Print the psu stats")
parser.add_option("-F", "--fc-port", action="store_true", dest="fc", default=False, help="Print the fc-ports stats")

parser.add_option("-C", "--community", action="store", type="string", dest="community", default="public", help="The snmpv2 community to use (default: public)")
parser.add_option("-H", "--host", action="store", type="string", dest="host", default="127.0.0.1", help="The ip of the host (default: 127.0.0.1)")

(opt, args) = parser.parse_args()
test = sum([(1 if x == True else 0) for x in [opt.type, opt.temp, opt.fan, opt.psu, opt.fc]])

if test != 1:
	print "You must specify only one display option!"

if opt.temp:
	exit(check_sensor("TEMP", "TEMP", "port", opt.host, opt.community))
elif opt.fan:
	exit(check_sensor("FAN", "FAN", "fan", opt.host, opt.community))
elif opt.psu:
	exit(check_sensor("Power Supply", "PSU", "", opt.host, opt.community))
elif opt.type:
	exit(check_type(opt.host, opt.community))
elif opt.fc:
	exit(check_fc_ports(opt.host, opt.community))
