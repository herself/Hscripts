#!/usr/bin/env bash
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Allows using a screen locker with the awesome ,,unclutter'' utility
##############

killall unclutter
#the locker
xlock -erasemode no_fade
unclutter -visible -grab&
