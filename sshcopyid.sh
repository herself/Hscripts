#!/usr/bin/env sh
# Author : Wiesław Herr (herself@makhleb.net)
# Check the included LICENSE file for licensing information
#
# Copy an ssh key to a remote machine when ssh-copy-id is unavailable
# or the service is running on a non-default port.
##############

cat ~/.ssh/id_rsa.pub | ssh $@ "mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys"
