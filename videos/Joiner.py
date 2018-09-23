# A programme that joins all .wav files in the current directory. Meant to overcome the size limitation of shnjoin. Still limited to 4GB, since that is a limitation of the format.

import sys
import os
import struct

debug = True

NL = "\n"
TB = "\t"

maxWavSize = 4294967296

channels = 2
samplerate = 44100
samplesize = 2
bytesPerSecond = channels*samplerate*samplesize
sizeThusFar = 0
totalSize = 0
chunkSize = 33554432
outFileName = "joined.wav"
outFile = open(outFileName, 'wb')
readBuffer = ""
writeRF64 = False

def Debug(inTxt):
 if debug: print ("--Debug: " + str(inTxt))

curDirContents = os.listdir(".")
curDirContents.sort()
# A header tuple contains: filename, format, #channels, samples per second, bytes per second, bytes per sample, bytes of PCM data.
headerData = []

files = []

for i in curDirContents:
 if i.endswith(".wav"):
   files.append(i)

files.remove(outFileName)
Debug(files)

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
 totalSize += i[6]

print "These wave files have " + str(channels) + " channels and are sampled at " + str(samplerate) + " Hz, " + str(samplesize) + " bytes per sample."

if totalSize < maxWavSize:
  outFile.write(struct.pack("4sI4s4sIHHIIHH4sI", "RIFF", 36+ totalSize, "WAVE", "fmt ", 16, 1, channels, samplerate, samplerate*channels*samplesize, channels*samplesize, samplesize*8, "data", totalSize))

else:
  outFile.write(struct.pack("<4si4s4sIQQQII4sIHHIIHHH22s4si", "RF64", -1, "WAVE", "ds64", 32, totalSize + 36, totalSize, totalSize/(samplesize), 0, 0, "fmt ", 40, 1, channels, samplerate, samplerate*channels*samplesize, channels*samplesize, samplesize*8, 22, "22randomcharsforfiller", "data", -1))
  print "It's a big one! RF64! This feature not guaranteed to work... It did in at least one case, though!"

for i in headerData:
 print "Now joining " + i[0] + "."
 curFile = open(i[0], 'rb')
 curFile.seek(44)
 readBuffer = curFile.read(chunkSize)
 while not readBuffer == "":
   outFile.write(readBuffer)
   readBuffer = curFile.read(chunkSize)
 sizeThusFar += i[6]
 curFile.close()
 outFile.flush()
outFile.close()
print "Joining done, " + str(sizeThusFar) + " bytes (" + str(sizeThusFar/1048576) + " megabytes) written into " + outFileName + "."

