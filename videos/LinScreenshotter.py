#!/usr/bin/env python3

import os
import sys
import shlex
import time
import signal
from subprocess import Popen, PIPE

class LinScreenshotter:
    def __init__(self, windowName):
        self.windowName = windowName
        self.imageCount = 0
        self.digits = 10
        self.prefix = windowName
        self.fileSuffix = ".png"
        curDate = time.localtime()
        self.dateStr = "".join([str(curDate.tm_year), str(curDate.tm_mon), str(curDate.tm_mday), str(curDate.tm_min), str(curDate.tm_min), str(curDate.tm_sec)])
        self.dirName = "-".join([self.prefix, self.dateStr])
        self.windowIDCommand = "xwininfo -root -tree | grep {}".format(windowName)
        self.windowID = ""
        self.screenshotCommand = "import -window {} {}"
        self.interval = 1
        self.exitNext = False
        self.compressMore = True
        self.compressCommand = "pngout {}"
        self.deduplicate = True
        self.hashCommand = "shasum {}"
        self.hashes = set()

    def initDir(self):
        cmd = "mkdir {}".format(self.dirName)
        process = Popen(cmd, shell=True)
        exitCode = process.wait()


    def setExit(self, bleh, blah):
        self.exitNext = True

    def getID(self):
        cmd = self.windowIDCommand
        while True:
            process = Popen(cmd, stdout=PIPE, shell=True, stdin=None, stderr=None)
            theOutput = process.communicate()[0]
            exitCode = process.wait()
            self.windowID = str(theOutput.split()[0])[1:]
            if exitCode != 0:
                time.sleep(self.interval)
            else:
                break

    def getScreenshot(self):
        while True:
            shotFilename = os.path.join(self.dirName, "".join([self.prefix, str(self.imageCount).zfill(self.digits), self.fileSuffix]))
            cmd = self.screenshotCommand.format(self.windowID, shotFilename)
            process = Popen(cmd, shell=True)
            exitCode = process.wait()
            if not exitCode:
                doCompress = False
                if self.deduplicate:
                    hashCmd = self.hashCommand.format(shotFilename)
                    process = Popen(hashCmd, stdout=PIPE, shell=True)
                    newHash = process.communicate()[0].split()[0]
                    exitCode = process.wait()
                    print(newHash)
                    if not exitCode and newHash not in self.hashes:
                        self.imageCount += 1
                        self.hashes.add(newHash)
                        doCompress = True
                else:
                    self.imageCount += 1
                    doCompress = True
                if self.compressMore and doCompress:
                    compressCmd = self.compressCommand.format(shotFilename)
                    process = Popen(compressCmd, shell=True)
                    exitCode = process.wait()
            if self.exitNext:
                exit()
            else:
                time.sleep(self.interval)

    def run(self):
        self.initDir()
        while True:
            try:
                self.getID()
                self.getScreenshot()
            except:
                pass
            if self.exitNext:
                exit()

if __name__ == "__main__":
    capturer = LinScreenshotter(sys.argv[1])
    signal.signal(signal.SIGINT, capturer.setExit)
    capturer.run()
