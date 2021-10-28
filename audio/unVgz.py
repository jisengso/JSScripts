#!/usr/bin/env python3
"""
$0 {vgzDirectory}

Takes a directory, finds all files ending with .vgz, converts them to .vgm. If no directory is provided, assumes current directory.

Dependency:
    - gunzip
"""

import sys
import os

vgzDirectory = "."
if len(sys.argv) == 2:
    vgzDirectory = sys.argv[1]

fileList = os.listdir(vgzDirectory)
vgzList = []

for listedFile in fileList:
    if listedFile.endswith(".vgz"):
        vgzList.append(listedFile)

if not len(vgzList):
    print("No .vgz files found! Exiting.")
    exit()

for vgzFile in vgzList:
    newName = vgzFile.replace(".vgz", ".vgm.gz")
    os.system(f"mv \"{vgzFile}\" \"{newName}\"")
    os.system(f"gunzip \"{newName}\"")

print("All .vgz files should be unpacked.")