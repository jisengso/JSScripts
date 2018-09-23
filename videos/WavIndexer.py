# A programme to create an index in hours, minutes, and seconds if all .wav files in the current directory are joined together in order. Also displays track's length in seconds if -s is used on command line.

import sys
import os
import struct

debug = False

NL = "\n"
TB = "\t"

displayTrackSecs = False
displayTimeList = False
removeZZZinList = False
removeZZZ = False

channels = 2
samplerate = 44100
samplesize = 2
bytesPerSecond = channels*samplerate*samplesize
sizeThusFar = 0

# This is key to proper timing with different framerates. 1 is good for 1FPS. 6 is good for 6FPS.
frameGranularity = 60

timeList = []

def Debug(inTxt):
 if debug: print ("--Debug: " + str(inTxt))

curDirContents = os.listdir(".")
curDirContents.sort()
# A header tuple contains: filename, format, #channels, samples per second, bytes per second, bytes per sample, bytes of PCM data.
headerData = []

files = []

if sys.argv.__contains__("-s"):
 displayTrackSecs = True

if sys.argv.__contains__("-t"):
 displayTimeList = True

if sys.argv.__contains__("-z"):
 removeZZZinList = True
 
if sys.argv.__contains__("-Z"):
 removeZZZ = True

for i in curDirContents:
 if i.endswith(".wav"):
   files.append(i)

for i in files:
 theFile = open(i, 'rb')
 rawData = theFile.read(44)
 udTmp = struct.unpack('4sI4s4sIHHIIHH4sI', rawData)
 relevantData = [udTmp[5], udTmp[6], udTmp[7], udTmp[8], udTmp[10]/8, udTmp[12]]
 headerData.append([i] + relevantData)

channels, samplerate, samplesize, bytesPerSecond = headerData[0][2], headerData[0][3], headerData[0][5], headerData[0][4]

for i in headerData:
 Debug(i)
 if i[1] != 1:
   quit(i[0] + " is not a canonical WAV/PCM file.")
 if channels != i[2]:
   quit(i[0] + " has a different number of channels.")
 if samplerate != i[3]:
   quit(i[0] + " has a different sample rate.")
 if samplesize != i[5]:
   quit(i[0] + " has a different sample size.")

for i in headerData:
 outString = ""
 curTime = sizeThusFar/bytesPerSecond
 curFrame = (sizeThusFar*frameGranularity)/bytesPerSecond
 hours = curTime/3600
 minutes = (curTime % 3600) /60
 seconds = curTime % 60
 nameTimeSet = [i[0], ((sizeThusFar + i[6])/bytesPerSecond) - curTime, (((sizeThusFar + i[6])*frameGranularity)/bytesPerSecond) - curFrame]
 
 # if hours != 0:
 outString += str(hours) + ":"
 outString += "%02d:" % minutes + "%02d " % seconds + TB + i[0]
 if displayTrackSecs:
   outString += TB + str(nameTimeSet[1])
 if displayTimeList:
   if removeZZZinList:
     if nameTimeSet[0].__contains__("zzz"):
       timeList[timeList.__len__()-1] += nameTimeSet[2]
     else:
       timeList.append(nameTimeSet[2])
   else:
     timeList.append(nameTimeSet[2])
 if removeZZZ:
   if outString.__contains__("zzz"):
     outString = ""
 if outString != "":
   print outString
 sizeThusFar += i[6]
print "Total seconds: " + str(sizeThusFar/bytesPerSecond)

if displayTimeList:
  print timeList
