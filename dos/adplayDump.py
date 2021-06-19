#!/usr/bin/env python3
import argparse
import sys
import subprocess
import tempfile
import ctypes
import random
import os
import shutil
import threading
import time
from pathlib import Path

def initArgparse():
    parser = argparse.ArgumentParser(description="""
Given a list of files, dump all music to disk, including subsongs.

adplayDump.py -d {outDir} {*inputFiles}

For each file, look to see how many subsongs are present.
For each subsong, have a default limit of 10 seconds to dump wav. adplay doesn't always know when a song ends.
Call upon sox to determine if the dumped wav was music and clip trailing silence.
""")
    parser.add_argument("-d", type=str, default="./", metavar="outDir", help="output directory (default: ./)")
    parser.add_argument("-u", type=int, default=0, metavar="subsongUpperBound", help="Max subsong number. (default: none)")
    parser.add_argument("-l", type=int, default=0, metavar="subsongLowerBound", help="Min subsong number. (default: none)")
    parser.add_argument("inputFiles", nargs="+", help="Files to convert (required)")
    args = parser.parse_args()
    return args

def getSubsongsNum(inputFile):
    infoFile = f"/dev/shm/.dump{random.random()}.txt"
    command = f"adplay -ro -O null {inputFile} 2> {infoFile}"
    information = ""
    subprocess.run(command, shell=True, timeout=1)
    with open(infoFile, "rb") as songInfoTmpFile:
        information = songInfoTmpFile.read()
    os.unlink(infoFile)
    subsongStartIdx = information.find(b"Subsong")
    subsongEndIdx = information.find(b",", subsongStartIdx)
    subsongSlice = information[subsongStartIdx:subsongEndIdx]
    dividerIdx = subsongSlice.find(b"/")
    numSubsongs = int(subsongSlice[dividerIdx+1:])
    return numSubsongs

def dumpSong(inputFile, subsongNum, outDir):
    print(f"Dumping {inputFile} subsong {subsongNum}")
    tmpOutFile = f"/dev/shm/.wavdump{random.random()}.wav"
    tmpFilteredFile = f"{tmpOutFile}.filtered.wav"
    dumpCommand = f"adplay {inputFile} -oq --surround -f 96000 -O disk -d {tmpOutFile} -s{subsongNum}"
    filterCommand = f"sox {tmpOutFile} {tmpFilteredFile} silence 0 1 10.0 0%"
    minimumSizeThreshold = 4096 #bytes
    aJunkFile = tempfile.TemporaryFile()
    playerProcess = subprocess.Popen(dumpCommand, shell=True, stderr=aJunkFile, stdout=aJunkFile)    
    try:
        playerProcess.wait(10)
    except subprocess.TimeoutExpired:
        playerProcess.terminate()
    aJunkFile.close()
    subprocess.run(filterCommand, shell=True)
    os.unlink(tmpOutFile)
    filteredFileSize = Path(tmpFilteredFile).stat().st_size
    print(f"{tmpFilteredFile} is {filteredFileSize} bytes.")
    if filteredFileSize < minimumSizeThreshold:
        print(f"Below minimum threshold, deleted.")
        os.unlink(tmpFilteredFile)
        return False
    else:
        newFilename = f"{inputFile}.{subsongNum:03}.wav"
        newDestination = f"{outDir}/{newFilename}"
        shutil.move(tmpFilteredFile, newDestination)
        print("Successfully dumped:", newFilename)
        return True

    

def dumpSongs(inputFile, outDir, args):
    subsongs = getSubsongsNum(inputFile)
    minSubsongs = args.l
    maxSubsongs = subsongs
    if args.u:
        maxSubsongs = args.u
    for subsongNum in range(minSubsongs, maxSubsongs):
        gotSong = dumpSong(inputFile, subsongNum, outDir)



def main():
    args = initArgparse()
    outDir = args.d
    inputFiles = args.inputFiles
    for eachFile in inputFiles:
        dumpSongs(eachFile, outDir, args)

if __name__ == "__main__":
    main()