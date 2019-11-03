#!/usr/bin/python3
"""
Extracts audio from all mkv, mp4, webm files in present directory, placing it in mka files with the same name in "./Audio" . 
Avoids overwriting existing files.

Depends on mkvmerge.

Usage:
audioExtract.py | bash
audioExtract.py . | bash
"""
import os
import sys
from pathlib import PurePath

class Entry:
    def __init__(self, filename):
        splitContents = filename.rsplit(".", 1)
        if len(splitContents) is 1:
            self.basename = splitContents[0]
            self.extension = ""
        if len(splitContents) is 2:
            self.basename, self.extension = splitContents
    def __eq__(self, other):
        result = False
        if self.basename == other.basename and self.extension == other.extension:
            result = True
        return result
    def __str__(self):
        return f"{self.basename}.{self.extension}"
    def __repr__(self):
        return self.__str__()

def findEntry(entryList, basename):
    for entry in entryList:
        if entry.basename == basename:
            return entry
    return None

curDir = PurePath(".")
if len(sys.argv) == 2:
    curDir = PurePath(sys.argv[1])
audioDir = curDir / "Audio"
curDirList = os.listdir(curDir)
if "Audio" not in curDirList:
    os.mkdir("Audio")
audioDirList = os.listdir(audioDir)
videoEntriesList = []
audioEntriesList = []
filenameHashSet = set()
toEncodeList = []
videoFileExtensions = ("mkv", "mp4", "webm")

for eachFileName in curDirList:
    theEntry = Entry(eachFileName)
    if theEntry.extension in videoFileExtensions:
        videoEntriesList.append(theEntry)
        filenameHashSet.add(theEntry.basename)

for eachFileName in audioDirList:
    theEntry = Entry(eachFileName)
    if theEntry.extension in ("mka",):
        audioEntriesList.append(theEntry)
        if theEntry.basename not in filenameHashSet:
            toEncodeList.append(theEntry)

for eachEntry in videoEntriesList:
    if not findEntry(audioEntriesList, eachEntry.basename):
        toEncodeList.append(eachEntry)

for eachVideoEntry in toEncodeList:
    videoEntry = findEntry(videoEntriesList, eachVideoEntry.basename)
    audioEntry = Entry(f"{videoEntry.basename}.mka")
    command = f"mkvmerge --no-video \"{videoEntry}\" -o \"{audioDir}/{audioEntry}\""
    print(command)
