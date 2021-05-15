#!/usr/bin/env python3
"""
Extracts Westwood .PAK files
Tested on Lands of Lore: The Throne of Chaos
"""
import sys
import struct

def readHeader(archiveContents):
    fileIndices = []

    sliceBegin = 0
    sliceEnd = 20
    segmentFormat = "<I12sI"
    keepSlicing = True
    while keepSlicing:
        curSegment = archiveContents[sliceBegin:sliceEnd]
        fileStart, fileName, fileEnd = struct.unpack(segmentFormat, curSegment)
        if fileName[0] == 0:
            keepSlicing = False
            break
        fileInfo = (fileStart, fileEnd, fileName)
        fileIndices.append(fileInfo)
        sliceBegin += 16
        sliceEnd += 16
    return fileIndices

def extractFile(archiveContents, fileInfo):
    sliceBegin = fileInfo[0]
    sliceEnd = fileInfo[1]
    fileName = fileInfo[2].replace(b"\x00", b"").decode("utf-8")
    exportFolder = "."
    print(f"{sliceBegin}, {sliceEnd}, {fileName}")
    writeContents = archiveContents[sliceBegin:sliceEnd]
    openPath = f"{exportFolder}/{fileName}"
    with open(openPath, "wb") as outFile:
        outFile.write(writeContents)
    print(f"{openPath} written.", file=sys.stderr)

def main():
    PAKFile = sys.argv[1]
    archiveContents = ""
    with open(PAKFile, "rb") as theFile:
        archiveContents = theFile.read()
    
    fileIndices = readHeader(archiveContents)
    for fileInfo in fileIndices:
        extractFile(archiveContents, fileInfo)

if __name__ == "__main__":
    main()