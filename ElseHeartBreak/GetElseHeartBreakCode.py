#!/usr/bin/env python3

"""
Exports Sprak code from Else Heart.Break() saved games that is marked with
"ExportMark".
"""

import sys
import json

class HeartBreakDevice:
    def __init__(self, deviceName, deviceContents):
        self.deviceName = deviceName
        self.deviceContents = deviceContents

def findSprak(saveFilename):
    fileContents = ""
    sprakEntries = []
    with open(saveFilename, "r") as sprakFile:
        fileContents = sprakFile.read()
    for lineEntry in fileContents.split("\n"):
        if "ExportMark" in lineEntry:
            sprakEntries.append(lineEntry)
    return sprakEntries

def cleanSprak(entriesList):
    cleanedCode = []
    for entry in entriesList:
        jsonEntry = json.loads(entry)
        deviceName = jsonEntry["values"][1].replace("\"", "")
        deviceContents = jsonEntry["values"][4].replace("\\n", "\n").replace("\\\"", "\"")[1:-2]
        cleanedCode.append(HeartBreakDevice(deviceName, deviceContents))
    return cleanedCode

def saveSprak(cleanedCode):
    for device in cleanedCode:
        filename = device.deviceName + ".sprak"
        contents = device.deviceContents
        try:
            with open(filename, "w") as sprakCodeFile:
                sprakCodeFile.write(contents)
                print("Saved " + filename)
        except:
            print("Couldn't save " + filename)

def main():
    if len(sys.argv) != 2:
        print("Need filename of saved game.")
        exit(1)
    sprakEntries = findSprak(sys.argv[1])
    cleanedCode = cleanSprak(sprakEntries)
    saveSprak(cleanedCode)
    print("Done, hopefully.")

if __name__ == "__main__":
    main()
