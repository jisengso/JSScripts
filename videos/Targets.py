# A small programme to make many symlinks to a few images for a video, mostly for encoding music with mplayer.
# This is aimed mostly at Linux, and anything else that supports symlinks.

import os
import sys

dirContents = os.listdir(".")

mainTxt = "ln -s "
parentDir = "../"
tFilePre = "Rome_"
targetNumberStart = 1
tFileSuf = ".png"
# targets is an array with numbers of frames per target image.
targets = [10877, 3818, 4229, 4958, 5128, 4980, 5270, 4849, 5361, 5326, 3739, 7934, 6640, 11467, 8017, 4845, 8340, 7525, 8409, 9929, 7368, 10488, 9445, 8358, 6942, 9629, 8340, 13094, 10335, 12015, 5378, 3571, 4849, 1204, 4730, 5438, 3271, 16559]
imgDir = "tgtImgs/"
filePre = "pointer"
cnt = 0
fileSuf = tFileSuf
SP = " "
# loopFrames allows the sequence of frames to start over, basically looping the video. maxFrames breaks this loop.
loopFrames = False
maxFrames = 12775

if not dirContents.__contains__(imgDir): 
	print "mkdir " + imgDir
else: 
	imgDirCont = os.listdir(imgDir)
	if imgDirCont.__len__() > 0: print "rm " + imgDir + "*"
def makeOutput():
 tNum = targetNumberStart
 global cnt
 for i in targets:
   for j in xrange(i):
     print mainTxt + parentDir + tFilePre + "%06d" % tNum + tFileSuf + SP + imgDir + filePre + "%07d" % cnt + fileSuf
     cnt = cnt + 1
     if loopFrames and cnt > maxFrames: quit()
   tNum += 1

while loopFrames and cnt < maxFrames:
 makeOutput()

makeOutput()

