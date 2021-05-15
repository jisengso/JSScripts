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
    sliceEnd = 24
    segmentFormat = "<I12sI"
    keepSlicing = True
    while keepSlicing:

        curSegment = archiveContents[sliceBegin:sliceEnd]
        nullIndex = curSegment.index(b"\x00", 4)
        strLen = nullIndex - 4
        segmentFormat = "<I" + f"{(strLen+1)}s" + "I"
        fileStart, fileName, fileEnd = struct.unpack_from(segmentFormat, curSegment)
        if fileName[0] == 0:
            keepSlicing = False
            break
        fileInfo = (fileStart, fileEnd, fileName)
        fileIndices.append(fileInfo)
        offsetReduction = 16 - nullIndex -1
        sliceBegin += 16 - offsetReduction
        sliceEnd = sliceBegin + 24 
    return fileIndices

def extractFile(archiveContents, fileInfo):
    sliceBegin = fileInfo[0]
    sliceEnd = fileInfo[1]
    fileName = fileInfo[2].replace(b"\x00", b"").decode("utf-8")
    exportFolder = "."
    writeContents = archiveContents[sliceBegin:sliceEnd]
    openPath = f"{exportFolder}/{fileName}"
    with open(openPath, "wb") as outFile:
        outFile.write(writeContents)
    print(f"{openPath} written.", file=sys.stderr)

def main():
    PAKFile = sys.argv[1]
    archiveContents = ""
    print(f"Opening {PAKFile}.", file=sys.stderr)
    with open(PAKFile, "rb") as theFile:
        archiveContents = theFile.read()
    
    fileIndices = readHeader(archiveContents)
    for fileInfo in fileIndices:
        extractFile(archiveContents, fileInfo)

if __name__ == "__main__":
    main()