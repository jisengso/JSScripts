#!/usr/bin/env python3
description = """
# Files dereduplicator

-d directory -j (JSON_filename)

Input: Directory with a bunch of files, assuming that duplicates exist.
Output: Deletes duplicate files from directory except for the first one in filename order. Creates a JSON (default name "duplicates.json") in specified directory which maps the files to duplicates.

-r directory -j (JSON_filename)

Input: Directory with deduplicated files and the JSON file.
Output: Copies the first file into all the duplicates.

-c directory

Input: Directory with a bunch of files.
Output: Count of duplicate files.

This program deduplicates files with hashibly identical contents, creating a map of files where the first file is related to all files with duplicate contents.

It can then reduplicate files with the same names. 

## Why use this program?

The directory contents can be made more compressible, or each file can be deterministically processed by some other program once instead of (n+1) times, where n is the number of duplicates. 

"""

import os
import hashlib
import sys
import json
import argparse

class Dereduplicator:
    def __init__(self, action, directory, jsonFilename):
        self.action = action
        self.directory = directory
        os.chdir(self.directory)
        self.jsonFilename = jsonFilename
        self.dupMap = {}
        self.dupCount = 0

    def calcDups(self):
        directoryContents = os.scandir(self.directory)
        fileList = []
        for eachFile in directoryContents:
            if eachFile.is_file:
                fileList.append(eachFile.name)
        hashMap = {}
        for eachFile in fileList:
            with open(eachFile, "rb") as fileContents:
                theHash = hashlib.sha3_512(fileContents.read()).hexdigest()
                if theHash not in hashMap:
                    hashMap[theHash] = [eachFile]
                else:
                    hashMap[theHash].append(eachFile)
        for eachHash in hashMap:
            hashMap[eachHash].sort()
            instanceNum = len(hashMap[eachHash])
            self.dupCount += instanceNum-1
            if instanceNum > 1:
                self.dupMap[hashMap[eachHash][0]] = hashMap[eachHash][1:]

        print (f"There are {self.dupCount} duplicate files.")

    def deduplicate(self):
        self.calcDups()

        jsonOutput = json.dumps(self.dupMap)
        with open(self.jsonFilename, "w") as outFile:
            outFile.write(jsonOutput)
        for instance in self.dupMap.keys():
            for eachDuplicate in self.dupMap[instance]:
                os.remove(eachDuplicate)

    def reduplicate(self):
        jsonContents = ""
        with open(self.jsonFilename, "r") as inFile:
            jsonContents = inFile.read()
        self.dupMap = json.loads(jsonContents)
        for instance in self.dupMap.keys():
            originalFileContents = b""
            with open(instance, "rb") as originalFile:
                originalFileContents = originalFile.read()
            for eachDuplicate in self.dupMap[instance]:
                with open(eachDuplicate, "wb") as dupFile:
                    dupFile.write(originalFileContents)


    def run(self):
        if self.action == 1:
            self.deduplicate()
        elif self.action == 2:
            self.reduplicate()
        elif self.action == 3:
            self.calcDups()

def parseArguments():
    if len(sys.argv) == 1:
        print (description)
        print ("No action specified.")
        return False
    action = 0
    directory = ""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', help='Directory to deduplicate')
    parser.add_argument('-r', help='Directory to reduplicate')
    parser.add_argument('-c', help='Directory to evaluate')
    parser.add_argument('-j', default="duplicates.json")
    args = parser.parse_args()
    if args.d or args.r or args.c:
        if args.d:
            action = 1
            directory = args.d
        elif args.r:
            action = 2
            directory = args.r
        elif args.c:
            action = 3
            directory = args.c
        return (action, directory, args.j)
    else:
        print("No action specified.")
        return False

if __name__ == "__main__":
    args = parseArguments()
    print(args)
    if not args:
        exit()
    deduper = Dereduplicator(*args)
    deduper.run()