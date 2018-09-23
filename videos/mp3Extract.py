# Finds MP3's in the file and extracts them, hopefully. Written for Rome: Total War.
# Magic number: \x49\x44\x33\x03
# Relies on files being packed tightly without compression nor encryption.
# Created 20150411
# By Jiseng So

srcFilename = "Music.dat"
srcFile = open(srcFilename, "r")
srcContents = srcFile.read()
mp3MagicNumber = "\x49\x44\x33\x03"
count = 1
moreStuff = True
mp3Indices = []
curIndex = -1

while moreStuff:
  nextIndex = srcContents.find(mp3MagicNumber, curIndex+1)
  if nextIndex == -1: 
    moreStuff = False
    mp3Indices.append(srcContents.__len__())
    break
  curIndex = nextIndex  
  mp3Indices.append(curIndex)
  
for i in range(mp3Indices.__len__()-1):
  outputFilename = "mp3Extract%03d" % count + ".mp3"
  count +=1
  outputFile = open(outputFilename, "wb")
  outputFile.write(srcContents[mp3Indices[i]:mp3Indices[i+1]])
  outputFile.close()