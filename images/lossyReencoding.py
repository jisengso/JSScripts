#/bin/env python3
"""
$0 {filename}

Outputs a series of JPEGs, illustrating the gradual decrease of visual quality.
"""
import os
import sys
from pathlib import PurePath
from subprocess import Popen, PIPE

def execute(command):
    print("execute: " + command)
    process = Popen(command, shell=True)
    exitCode = process.wait()

convertSteps = 10000
originalFilename = sys.argv[1]
originalStem = PurePath(originalFilename).stem
originalExtension = PurePath(originalFilename).suffix
subDirectory = f"{originalStem}-lossy"
makeSubdir = f"mkdir {subDirectory}"
firstStep = f"convert {originalFilename} -quality 90 {subDirectory}/{originalStem}00000.jpeg"

execute(makeSubdir)
execute(firstStep)

for iteration in range(convertSteps):
    fromFile = f"{subDirectory}/{originalStem}{iteration:05}.jpeg"
    toFile = f"{subDirectory}/{originalStem}{iteration+1:05}.jpeg"
    command = f"convert {fromFile} -quality 90 {toFile}"
    execute(command)