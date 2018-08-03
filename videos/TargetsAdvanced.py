#!/usr/bin/python

import os
import sys


# Sequence types: single-image, multi-image evenly timed, looping, manual intervals
# 1: single-image               ["floofy.wav", 700, 1, "floofy.png"]
# 2: multi-image evenly timed   ["floofSlide.wav", 400, 2, "floofSlide/"]
# 3: looping                    ["Floofloop.wav", 300, 3, "floofLoop/", 30]
# 4: manual intervals           ["floofMov.wav", 600, 4, "floofMov/", [120, 60, 20, 200]]
# With manual intervals, specify frame lengths for all images except last one, which will last for the remaining frames
# WAV filename, WAV video frame length, sequence type, corresponding directory or image file, [manual intervals]
# For directories, it is expected that the contents are images arranged alphabetically/numerically in the order they will be displayed

command = "ln -s "
curFrame = 1
tFileSuf = ".png"
parentDir = "../"
imgDir = "tgtImgs/"
filePre = "pointer"
SP = " "
NL = "\n"
dirContents = os.listdir(".")


sequences = [['01 Steal the sky.wav', 1682, 4, "01Steal/", [96, 48]],
['02 INTRO1.wav', 360, 2, "02Intro/"],
['03 INTRO2.wav', 310, 2, "03Intro/"],
['04 INTRO3.wav', 518, 2, "04Intro/"],
['05 INTRO4.wav', 318, 2, "05Intro/"],
['06 REBEL.wav', 457, 2, "06Intro/"],
['07 BASE1.wav', 437, 2, "07Base/"],
['08 BASE2.wav', 235, 2, "08Base/"],
['09 TUNNEL.wav', 214, 2, "09Tunnel/"],
['10 INTRO5.wav', 314, 2, "10Intro/"],
['11 INTRO6.wav', 186, 2, "11Intro/"],
['12 INTRO7.wav', 282, 2, "12Intro/"],
['13 choiseDOS.wav', 248, 1, "13Choise.png"],
['14 choise.wav', 223, 2, "14Choise/"],
['15 main1dos.wav', 1716, 2, "15Main1Adlib/"],
['16 main1.wav', 2730, 2, "16Main1Mod/"],
['17 main2dos.wav', 1490, 2, "17Main2Adlib/"],
['18 main2.wav', 2770, 2, "18Main2Mod/"],
['19 talkDOS.wav', 1590, 1, "19TalkAdlib.png"],
['20 talk.wav', 1244, 1, "20TalkMod.png"],
['21 event1dos.wav', 354, 1, "21Event1.png"],
['22 spaceDOS.wav', 336, 2, "22SpaceAdlib/"],
['23 space.wav', 722, 2, "23SpaceMod/"],
['24 earthDOS.wav', 1122, 1, "24EarthAdlib.png"],
['25 earth.wav', 735, 1, "25EarthMod.png"],
['26 event2dos.wav', 322, 1, "26Event2.png"],
['27 event3dos.wav', 258, 1, "27Event3.png"],
['28 failureDOS.wav', 416, 2, "28FailureAdlib/"],
['29 failure.wav', 356, 1, "29FailureMod.png"],
['30 reu-win.wav', 789, 2, "30Victory/"]]

output = []

if not dirContents.__contains__(imgDir): 
    output.append("mkdir " + imgDir)

for sequence in sequences:
    if sequence[2] == 1:
        for frameNo in range(sequence[1]):
            output.append(command + parentDir + sequence[3] + SP + imgDir + filePre + "%07d" % curFrame + tFileSuf)
            curFrame+=1
    if sequence[2] == 2:
        dirContents = os.listdir(sequence[3])
        sequenceContents = []
        for i in dirContents:
            if i.endswith(tFileSuf):
                sequenceContents.append(i)
        sequenceContents.sort()
        interval = sequence[1] / sequenceContents.__len__()
        curImageNo = 0
        curImage = ""
        for frameNo in range(sequence[1]):
            if frameNo < sequence[1] - (interval-1):
                curImageNo = frameNo/interval
                curImage = sequenceContents[curImageNo]
            output.append(command + parentDir + sequence[3] + curImage + SP + imgDir + filePre + "%07d" % curFrame + tFileSuf)            
            curFrame+=1
    if sequence[2] == 3:
        dirContents = os.listdir(sequence[3])
        sequenceContents = []
        for i in dirContents:
            if i.endswith(tFileSuf):
                sequenceContents.append(i)
        sequenceContents.sort()
        interval = sequence[4]
        numImages = sequenceContents.__len__()
        curImageNo = 0
        curImage = ""
        for frameNo in range(sequence[1]):
            if frameNol < sequence[1] - interval:
                curImageNo = (frameNo/interval) % numImages
                curImage = sequenceContents[curImageNo]
            output.append(command + parentDir + sequence[3] + curImage + SP + imgDir + filePre + "%07d" % curFrame + tFileSuf)            
            curFrame+=1
    if sequence[2] == 4:
        dirContents = os.listdir(sequence[3])
        sequenceContents = []
        for i in dirContents:
            if i.endswith(tFileSuf):
                sequenceContents.append(i)
        sequenceContents.sort()
        numImages = sequenceContents.__len__()
        curImageNo = 0
        curImage = ""
        timings = sequence[4]
        lastTiming = sequence[1]
        for i in timings:
            lastTiming -= i
        timings.append(lastTiming)
        for image in sequenceContents:
            imageIdx = sequenceContents.index(image)
            for frameNo in range(timings[imageIdx]):
                output.append(command + parentDir + sequence[3] + image + SP + imgDir + filePre + "%07d" % curFrame + tFileSuf)            
                curFrame+=1
for line in output:
    print line