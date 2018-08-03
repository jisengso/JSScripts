import os
import sys

fileList = os.listdir(".")
wavList = []
numWavs = 0
ZZZPath = "../"
ZZZFile = "ZZZ44.wav"
linkName = "zzz.wav"
outText = ""


for i in fileList:
  if i.__contains__(".wav"):
    wavList.append(i)

numWavs = wavList.__len__()

for i in range(numWavs):
  outText += "ln -s " + ZZZPath + ZZZFile + " %02d" % (i+1) + linkName + "\n"
  
print outText
