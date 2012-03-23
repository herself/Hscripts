#!/usr/bin/env bash
# Author : Wiesław Herr
# LICENSE unspecified
#
# Forces a rescan of SCSI devices, ie. FC driven disks
##############

for i in /sys/class/scsi_host/host*/scan; do echo "- - -" > $i; echo $i; done
