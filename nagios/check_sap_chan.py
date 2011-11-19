#!/usr/bin/env python
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# A nagios script which checks if all SAP channels are online
##############

import urllib2
import xml.etree.ElementTree
from optparse import OptionParser
from subprocess import Popen, PIPE
from sys import stdout, exit
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-H", "--host", action="store", type="string", dest="host", default="xp1app", help="The address of the host (default: xp1app)", metavar="HOST")
parser.add_option("-P", "--port", action="store", type="int", dest="port", default="53500", help="The port to connect to (default: 53500)", metavar="PORT")
(opt, args) = parser.parse_args()

URL = "http://%s:%d/AdapterFramework/ChannelAdminServlet?party=*&service=*&channel=*&action=status" % (opt.host, opt.port)

passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, uri=URL, user="pi_monitor", passwd="Lotos321")

auth_handler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(auth_handler)

urllib2.install_opener(opener)

xml_file = urllib2.urlopen(URL)
tree = xml.etree.ElementTree.parse(xml_file)

errors = [elem for elem in tree.getiterator("Channel") if elem.find("ChannelState") != None and elem.find("ChannelState").text == "ERROR"]
print_errors = ["P: %s, S: %s, CN: %s" % (elem.find("Party").text, elem.find("Service").text, elem.find("ChannelName").text) for elem in errors if elem.find("ChannelName").text != "RcvSoapOilTasOILORD"]

num_errors = len(print_errors)
if num_errors == 0:
	print "Channels OK"
else:
	print "%d channel errors!" % (num_errors)
	for x in print_errors:
		print x
	exit(1)
