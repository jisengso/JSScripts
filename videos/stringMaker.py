# stringMaker
# coding=utf-8
# A script that uses BMP fonts, a char map, width map, 
# and a list of strings to be rendered and renders them in BMP format.

from bmpHandler import bmpHandler
import subprocess
def Debug(inTxt):
  if debug: print("---debug: " + inTxt)

debug = True

hPadding = 0
vPadding = 2
bmpFontPath = "fontmap.bmp"
bmpFontIsFixedWidth = False
bmpFontFixedWidth = 13
charMapPath = ""
charMapIsFile = False
charMap = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ,-?'\""
placeholderChar = "|"
allCaps = True
interCharSpacing = 0
spaceWidth = bmpFontFixedWidth
widthMapPath = ""
widthMapIsFile = False
widthMap = []
charMapOffsets = []
charLookupTable = {}
stringAppend = "\nVideo by Jiseng So"
stringsToRenderPath = ""
stringsToRenderIsFile = False
stringsToRender = u"Title Theme\nFile Select\nPeach's Message\nOpening\nLakitu's Message\nToad's Message\nInside the Castle Walls\nGame Start\nMain Theme\nStage Boss\nPower Star\nStar Catch Fanfare\nCourse Clear\nPiranha Plant's Lullaby\nCorrect Solution\nSnow Mountain\nRace Fanfare\nSlider\nKoopa's Message\nKoopa's Road\nKoopa's Theme\nKoopa Clear\nPowerful Mario\nDire, Dire Docks\nCave Dungeon\nHaunted House\nMerry-Go-Round\nLethal Lava Land\nLooping Steps\nMetallic Mario\nUltimate Koopa\nUltimate Koopa Clear\nEnding Demo\nStaff Roll\n"
if allCaps:
  stringsToRender = stringsToRender.upper()
  stringAppend = stringAppend.upper()
stringsToRender += stringAppend
outputFilePath = "outputText.bmp"
stringList = stringsToRender.split("\n")

perPhraseDir = "perPhrase"
subprocess.call(["mkdir", perPhraseDir])

# The charLookupTable is a dictionary which uses the char to lookup 
#   vertical and horizontal offsets relative to the fontMap.

if debug: 
  charMapR = ""
  for i in range(charMap.__len__()):
    charMapR += charMap[charMap.__len__() - i -1]
  stringList.append(charMapR)


  
bmpThingy = bmpHandler()
fontMap = bmpThingy.readBmp(bmpFontPath)
fontHeight = 0
fillPixel = fontMap[0][0]
finalHeight = 0
finalWidth = 0
finalPixMap = []

fillColorFile = open(perPhraseDir + "/" + "fillColor.txt", "w")
fillColorFile.write("#%0.2X%0.2X%0.2X" % fillPixel)
fillColorFile.write("\n")
fillColorFile.close()
    
def findVOffsets():
  # Finds the vertical offsets of the row of characters.
  # Basically measures the tallest character in that row.
  # This requires spaces between characters. If it's a solid line of characters up and down, this detection will fail.
  # Finite states:
  # 0 Initial, still finding just fill pixels. Goes to 1 when hit something else.
  #     Records position as top of tallest character in row upon state change.
  # 1 Hitting something with the traced line.
  #     Goes to 0 again when finding just fill pixels. Records position as bottom of character in row upon state change.

  findVState = 0
  vOffsets = []
  anOffset = [-1, -1]
  for i in range(fontMap.__len__()):
    isFullHLine = fullHLine(i)
    if findVState == 0:
      if not isFullHLine:
	anOffset[0] = i
	findVState = 1
    elif findVState == 1:
      if isFullHLine:
	anOffset[1] = i
	findVState = 0
	vOffsets.append(anOffset)
	anOffset = [-1, -1]

  if findVState == 1:
    anOffset[1] = fontMap.__len__()
    vOffsets.append(anOffset)

  return vOffsets

def fullHLine(yPos):
  # Cast a horizontal line, does it reach the end of the screen?
  result = True
  for i in fontMap[yPos]:
    if i != fillPixel:
      result = False
      break
  
  return result

def findHOffsets(startY, height):
  # Finds the horizontal offsets of the row of characters.
  # Basically measures the width of all characters.
  # This requires spaces between characters. If it's a solid line of characters side to side, this detection will fail.
  # Finite states:
  # 0 Initial, just fill pixels for the height of the row. 
  #   Goes to 1 when hits something and records the beginning of the character.
  # 1 Hitting something with vertical line. 
  #   When the line hits just fill pixels, switches back to state 0 and records end of character.
  findHState = 0
  hOffsets = []
  anOffset = [-1, -1]

  for i in range(fontMap[0].__len__()):
    isFullVLine = fullVLine(i, startY, height)
    if findHState == 0:
      if not isFullVLine:
	anOffset[0] = i
	findHState = 1
    elif findHState == 1:
      if isFullVLine:
	anOffset[1] = i
	findHState = 0
	hOffsets.append(anOffset)
	anOffset = [-1, -1]
    
  if findHState == 1:
    anOffset[1] = fontMap[0].__len__()
    hOffsets.append(anOffset)
  
  return hOffsets

def fullVLine(xPos, yPos, height):
  # Cast a vertical line in the row of text, does it go from top to bottom?
  result = True
  for i in range(height):
    if fontMap[i+yPos][xPos] != fillPixel:
      result = False
      break
  
  return result

def isEmptyCell(vOffset, hOffset):
  result = True
  for i in range(hOffset[1]-hOffset[0]):
    if not fullVLine(hOffset[0] + i, vOffset[0], vOffset[1] - vOffset[0]):
      result = False
      break
  return result  

charMapIndex = 0
vOffsets = findVOffsets()
initVOffset = vOffsets[0][0]
vSpaceBetweenChars = 9999
for i in range(vOffsets.__len__()-1):
  tmp = vOffsets[i+1][0] - vOffsets[i][1]
  if vSpaceBetweenChars > tmp: vSpaceBetweenChars = tmp
  height = vOffsets[i][1] - vOffsets[i][0]
  if height > fontHeight: fontHeight = height

Debug("vSpaceBetweenChars: " + str(vSpaceBetweenChars))
  
if fontHeight == 0:
  fontHeight = fontMap.__len__()

if bmpFontIsFixedWidth:
  hOffsets = findHOffsets(0, fontMap.__len__())
  for i in vOffsets:
    for j in hOffsets:
      Debug(charMap[charMapIndex] + " " + str(i) + ", " + str(j))
      if not isEmptyCell(i,j): 
	charLookupTable[charMap[charMapIndex]] = [i,j]
	charMapIndex+=1
else:
  for i in vOffsets:
    hOffsets = findHOffsets(i[0], i[1]-i[0])
    for j in hOffsets:
      if not isEmptyCell(i,j):
	Debug(charMap[charMapIndex])
	charLookupTable[charMap[charMapIndex]] = [i,j]
	charMapIndex+=1

finalHeight = fontHeight * stringList.__len__()
  
Debug("charLookupTable - " + str(charLookupTable))

for i in stringList:
  phraseWidth = 0
  if bmpFontIsFixedWidth:
    phraseWidth = i.__len__() * (bmpFontFixedWidth + interCharSpacing)
  else:
    for j in i:
      if j == " ": phraseWidth += spaceWidth + interCharSpacing
      else: phraseWidth += (charLookupTable[j][1][1] - charLookupTable[j][1][0]) + interCharSpacing
  if phraseWidth > finalWidth:
    finalWidth = phraseWidth

Debug("Final dimensions - " + str(finalWidth) + "x" + str(finalHeight))

Debug("charMap length: " + str(charMap.__len__()))

for i in range(stringList.__len__()):
  # i is the index number of the current phrase.
  curYoffset = i*(fontHeight + vPadding)
  curXoffset = 0

  phraseFilename = "%04d" % (i+1)
  phrasePixMap = []
  
  for j in range(fontHeight + vPadding):
    # j is a number here.
    # Creating the arrays vertically.
    finalPixMap.append([])
    phrasePixMap.append([])
  for j in stringList[i]:
    # j is the current letter in the phrase.
    currentLetter = j
    # Debug("Matching letter to index - " + currentLetter)
    currentLetterWidth = bmpFontFixedWidth
    currentLetterOffset = [[],[]]
    if j != u' ': currentLetterOffset = (charLookupTable[currentLetter][0][0], charLookupTable[currentLetter][1][0])
    if not bmpFontIsFixedWidth: 
      if j != u' ': currentLetterWidth = charLookupTable[currentLetter][1][1] - charLookupTable[currentLetter][1][0]
    for k in range(fontHeight + vPadding):
      # k is the vertical position in the current phrase's row.
      if k < fontHeight:
	for l in range(currentLetterWidth + interCharSpacing):
	  # l is the horizontal position
#	  Debug(str(currentLetterOffset) + " CLO: " + currentLetter + " kl: "+ str(k) + "," + str(l))
	  if j == u' ' or l > currentLetterWidth: transPixel = fillPixel
	  elif currentLetterOffset[0] + k >= fontMap.__len__(): transPixel = fillPixel
	  else:
	    transPixel = fontMap[currentLetterOffset[0] + k][currentLetterOffset[1] + l]
	  
	  finalPixMap[k + curYoffset].append(transPixel)
	  phrasePixMap[k].append(transPixel)
      else:
	for l in range(currentLetterWidth + interCharSpacing):
	  finalPixMap[k + curYoffset].append(fillPixel)
	  phrasePixMap[k].append(fillPixel)
    curXoffset += currentLetterWidth + interCharSpacing
  for j in range(fontHeight + vPadding):
    for k in range(finalWidth - curXoffset):
      finalPixMap[j + curYoffset].append(fillPixel)  
  bmpThingy.writeBmp(perPhraseDir + "/" + phraseFilename + ".bmp", phrasePixMap)
  
bmpThingy.writeBmp(outputFilePath, finalPixMap)
