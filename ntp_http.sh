#!/usr/bin/env bash
# Author : mina86 (http://mina86.com/2010/01/16/ntp-over-http/)
# LICENSE unspecified
#
# A very handy script to synchronize time through http headers when ntp is unavailable.
# Works well through NTLM proxies with cntlm.
##############

date -s "$(wget -S -O /dev/null google.com 2>&1 | sed -n -e '/  *Date: */ {' -e s///p -e q -e '}')"
