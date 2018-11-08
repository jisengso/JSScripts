# Maps random images from source directory with symlinks
# Created 20150410
# By Jiseng So

import os
import sys
import random

SP = " "
srcDir = "../Cheese/" #Relative to where the symlinks will be placed
tgtDir = "tgtImgs/" #Where the symlinks will be placed
prefix = "pointer"
extension = ".png"
startNum = 705
endNum = 1309

srcContents = os.listdir(srcDir.replace("../",""))
srcFiles = []

for i in srcContents:
  if i.endswith(extension): srcFiles.append(i)
  
for i in range(startNum, endNum+1):
  randImg = srcFiles[random.randint(0,srcFiles.__len__()-1)]
  print "ln -s -f " + srcDir + randImg + SP + tgtDir + prefix + "%07d" % i + extension