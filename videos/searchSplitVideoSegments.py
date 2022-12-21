#!/usr/bin/env python3

"""

Takes a video, srt file, and literal search term.

Outputs video clips which contain the search term.

-v {videoFilename}
-s {srtFilename}
-t {searchTerm}
-n {number of parallel processes}
-d Dummy run. Just tell me which subtitle lines match.

Dependencies:
    ffmpeg
    python3

Tips:
    KDENlive is able to use speech recognition to create srt subtitles.
    I assume the subtitle times are accurate.

Use case:
    Ever wanted to extract all the clips where someone said something? Now you can do it without uploading it to a random online service. This will do it losslessly!

Thoughts:
    Maybe could expand to regex.

Relies on srt format, which looks like:

Subtitle entry number
Start time --> end time
Text

Example:
4
00:01:00,510 --> 00:01:04,410
Rabbits eat hay!

"""

import getopt
import os
import sys
import string
from subprocess import Popen, PIPE
from multiprocessing import Pool

def execute(command):
    print("execute: " + command)
    process = Popen(command, shell=True)
    exitCode = process.wait()
    return exitCode

class Splitter:
    def __init__(self, vidName, srtName, searchTerm, numProcesses=1, dummyRun=False):
        self.videoFilename = vidName
        self.srtFilename = srtName
        self.searchTerm = searchTerm
        self.parallelProcesses = numProcesses
        self.dummyRun = dummyRun
        self.clipTimesList = []
        self.commandTemplate = "ffmpeg -i \"{videoFile}\" -ss {startTime} -to {endTime} -c:v copy -c:a copy -n \"{outputFile}\""

    def sanitize(self, dirtyPhrase):
        acceptableChars = string.ascii_letters + string.digits + "_"
        dirtyChars = list(set(dirtyPhrase))
        newPhrase = dirtyPhrase

        for char in dirtyChars:
            if char not in acceptableChars:
                if char in string.whitespace:
                    newPhrase = newPhrase.replace(char, "_")
                else:
                    newPhrase = newPhrase.replace(char, "")
        return newPhrase

    def search(self):
        allLines = []
        with open(self.srtFilename, "r") as subFile:
            allLines = subFile.readlines()
        for entry in zip(range(len(allLines)), allLines):
            currentLine = entry[0]
            entryText = entry[1].strip()
            clipTimes = allLines[currentLine - 1].strip()
            if self.searchTerm in entryText:
                self.clipTimesList.append([clipTimes, entryText])

                if self.dummyRun:
                    print(clipTimes, entryText)

    def split(self):
        commands = []
        outputDir = "splitClips"
        try:
            os.mkdir(outputDir)
        except:
            pass
        for entry in self.clipTimesList:
            startTime, endTime = entry[0].split(" --> ")
            startTime = startTime.replace(",", ".")
            endTime = endTime.replace(",", ".")

            timePrefix = startTime[:9].replace(":", "")
            phrase = entry[1]
            phrase = self.sanitize(phrase)
            outFile = f"{outputDir}/{timePrefix}_{phrase}.mkv"

            commandString = self.commandTemplate.format(videoFile=self.videoFilename, startTime=startTime, endTime=endTime, outputFile=outFile)
            commands.append(commandString)


        if self.dummyRun:
            for command in commands:
                print(command)
        else:
            with Pool(processes=self.parallelProcesses) as thePool:
                thePool.map(execute, commands)
                thePool.close()

    def run(self):
        self.search()
        self.split()

if __name__ == "__main__":
    shortOptions = "v:s:t:nd"
    opts, args = getopt.getopt(sys.argv[1:], shortOptions)

    print(opts, args)

    numProcesses = 1
    dummyRun = False
    videoFile = ""
    srtName = ""
    searchTerm = ""

    for opt, arg in opts:
        if opt == "-n":
            numProcesses = int(args[0]) # Oddly, getopt puts the argument in a different list.
        elif opt == "-d":
            dummyRun = True
        elif opt == "-v":
            videoFile = arg
        elif opt == "-s":
            srtName = arg
        elif opt == "-t":
            searchTerm = arg

    
    splittyThing = Splitter(videoFile, srtName, searchTerm, numProcesses, dummyRun)
    splittyThing.run()