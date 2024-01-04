#!/usr/bin/env python3
"""
$0 {highlyCompressibleTextfile}

This is meant to be a human-readable demonstration of how Lempel-Ziv works.
The "compressed" result cannot be uncompressed, due to ambiguity. It works well
on extremely repetitive text.
"""

import sys
import time
def doLempelZivCompress(thingToCompress):
    dictionary = []
    compressedOutput = []
    keepCompressing = True

    offset = 0
    length = 1
    endLength = len(thingToCompress)
    iteration = 0
    lastKnownSlice = -1
    while keepCompressing:
        compressSlice = thingToCompress[offset:offset+length]
        if compressSlice in dictionary:
            length += 1
            lastKnownSlice = dictionary.index(compressSlice)
        elif offset+length >= endLength:
            compressedOutput.append(compressSlice)
            keepCompressing = False
        else:
            dictionary.append(compressSlice)
            if compressSlice:
                compressedOutput.append(f"{lastKnownSlice}{compressSlice[-1]}")
            else:
                compressedOutput.append(f"{lastKnownSlice}{compressSlice}")
            offset += length
            length = 1
            lastKnownSlice = -1
        
        compressedString = ''.join(compressedOutput)

        print(f"Dictionary: {dictionary}")
        print(f"Window: {compressSlice}")
        print(f"compressedOutput: {compressedString}")
        print(f"Iteration: {iteration}")
        print(f"Offset: {offset}")
        print(f"Length: {length}")
        print(f"CompressedOutput length: {len(compressedString)}")
        print("\n")
        time.sleep(.1)
        iteration += 1

if __name__ == "__main__":
    fileToCompress = sys.argv[1]
    contentsToCompress = ""
    with open(fileToCompress, "r") as theFile:
        contentsToCompress = theFile.read()
    doLempelZivCompress(contentsToCompress)
