#!/usr/bin/env python3

# Chooses a random VPN from a list and creates a symlink to it.
# Meant to be used in conjunction with an autostarting OpenVPN setup.

import random
import os
import string


openVPNDir = "/etc/openvpn/"
selectListFilename = "selectionList.txt"
linkFilename = "selectedVPN.conf"
commandFormat = "ln -f -s \"{0}\" {1}"

os.system("cd " + openVPNDir)

selectListFile = open(selectListFilename, "r")
selectList = selectListFile.read().split("\n")
selectListFile.close()

chosenVPN = ""

while not chosenVPN:
    chosenVPN = random.choice(selectList).strip()

command = commandFormat.format(chosenVPN, linkFilename)

os.system(command)