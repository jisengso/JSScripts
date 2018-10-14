#!/usr/bin/env python3

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
        self.windowIDCommand = "xwininfo -root -tree | grep {}".format(windowName)
        self.windowID = ""
        self.screenshotCommand = "import -window {} {}"
        self.interval = 1
        self.exitNext = False
        self.compressCommand = "pngout {}"
        self.hashCommand = "shasum {}"
        self.hashes = set()
        signal.signal(signal.SIGINT, self.setExit)

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
            shotFilename = "".join([self.prefix, str(self.imageCount).zfill(self.digits), self.fileSuffix])
            cmd = self.screenshotCommand.format(self.windowID, shotFilename)
            process = Popen(cmd, shell=True)
            exitCode = process.wait()
            compressCmd = self.compressCommand.format(shotFilename)
            process = Popen(compressCmd, shell=True)
            process.wait()
            hashCmd = self.hashCommand.format(shotFilename)
            process = Popen(hashCmd, stdout=PIPE, shell=True)
            newHash = process.communicate()[0].split()[0]
            process.wait()
            print(newHash)
            if newHash not in self.hashes:
                self.imageCount += 1
                self.hashes.add(newHash)
            if exitCode != 0:
                return exitCode
            elif self.exitNext:
                exit()
            else:
                time.sleep(self.interval)

    def run(self):
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
    capturer.run()
