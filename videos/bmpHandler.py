import os
import struct
import sys

# A class to open and save BMPs. 
# Only handles 24-bit, uncompressed ones because I'm lazy.

class bmpHandler:
  def __init__(self):
# This is for the header.
    self.bfType = "BM"
    self.bfSize = 0
    self.bfReserved1 = 0
    self.bfReserved2 = 0
    self.bfOffBits = 54

    self.biSize = 40
    self.biWidth = 0
    self.biHeight = 0
    self.biPlanes = 1
    self.biBitCount = 24
    self.biCompression = 0
    self.biSizeImage = 0
    self.biXPelsPerMeter = 0
    self.biYPelsPerMeter = 0
    self.biClrUsed = 0
    self.biClrImportant = 0
  
    self.headerFmt = "<2sIHHI" + "IIIHHIIIIII"
    
    self.pixelData = []
    self.curPath = ""
# Now to read a BMP. One important thing to remember is that they're upside-down, compared to normal Cartesian coordinates.

  def readBmp(self, bmpPath):
    debug("readBmp " + bmpPath)
    fileBuffer = ""
    self.curPath = bmpPath
    bmpFile = open(self.curPath, 'rb')
    fileBuffer = bmpFile.read(54)
    readTuple = struct.unpack(self.headerFmt, fileBuffer)
    debug(readTuple)

    self.bfType = readTuple[0]
    self.bfSize = readTuple[1]
    self.bfReserved1 =  readTuple[2]
    self.bfReserved2 =  readTuple[3]
    self.bfOffBits =  readTuple[4]

    self.biSize =  readTuple[5]
    self.biWidth =  readTuple[6]
    self.biHeight =  readTuple[7]
    self.biPlanes =  readTuple[8]
    self.biBitCount =  readTuple[9]
    self.biCompression =  readTuple[10]
    self.biSizeImage =  readTuple[11]
    self.biXPelsPerMeter =  readTuple[12]
    self.biYPelsPerMeter =  readTuple[13]
    self.biClrUsed = readTuple[14]
    self.biClrImportant =  readTuple[15]
        
    self.pixelData = []
    rowPadding = self.biWidth % 4
    bmpFile.seek(self.bfOffBits)
    fileBuffer = bmpFile.read()
    bmpFile.close()
    for i in range(self.biHeight):
      rowData = []
      for j in range(self.biWidth):
	offset = (i*self.biWidth*3)+(j*3)+(i*rowPadding)
	#debug("offset " + str(offset))
	pixel = struct.unpack_from("BBB", fileBuffer, offset)
	rowData.append((pixel[2], pixel[1], pixel[0]))
      self.pixelData.append(rowData)
    self.pixelData.reverse()
    return self.pixelData

  def writeBmp(self, bmpPath, inPixData):
    debug("writeBmp " + bmpPath)
    writeStatus = False
    inPixData.reverse()
    self.curPath = bmpPath
    if self.verifyDimensions(inPixData):
      
      bmpFile = open(bmpPath, 'wb')
      self.pixelData = inPixData
      self.biSize = 40
      self.biWidth = inPixData[0].__len__()
      self.biHeight = inPixData.__len__()
      self.biPlanes = 1
      self.biBitCount = 24
      self.biCompression = 0
      rowPadding = self.biWidth % 4
      self.biSizeImage = ((self.biWidth *3)+ rowPadding) * self.biHeight
      self.biXPelsPerMeter = 2835
      self.biYPelsPerMeter = 2835
      self.biClrUsed = 0
      self.biClrImportant = 0
      
      self.bfType = "BM"
      self.bfSize = self.biSizeImage + 54
      self.bfReserved1 = 0
      self.bfReserved2 = 0
      self.bfOffBits = 54
      
      if self.biWidth == 0 or self.biHeight == 0:
        debug("Empty bitmap.")
        return False
      
      writeTuple = (self.bfType, self.bfSize, self.bfReserved1, self.bfReserved2, self.bfOffBits, self.biSize, self.biWidth, self.biHeight, self.biPlanes, self.biBitCount, self.biCompression, self.biSizeImage, self.biXPelsPerMeter, self.biYPelsPerMeter, self.biClrUsed, self.biClrImportant)

      debug(writeTuple)
      
      paddingString = struct.pack(str(rowPadding)+"x")
      mainString = ""
      
      for i in range(self.biHeight):
	rowString = ""
	for j in range(self.biWidth):
	  curPixel = self.pixelData[i][j]
	  pixelString = struct.pack("BBB", curPixel[2], curPixel[1], curPixel[0])
	  rowString = rowString + pixelString
	mainString = mainString + rowString + paddingString
      
      bmpFile.write(struct.pack(self.headerFmt, writeTuple[0], writeTuple[1], writeTuple[2], writeTuple[3], writeTuple[4], writeTuple[5], writeTuple[6], writeTuple[7], writeTuple[8], writeTuple[9], writeTuple[10], writeTuple[11], writeTuple[12], writeTuple[13], writeTuple[14], writeTuple[15]))
      bmpFile.write(mainString)
      bmpFile.close()
      writeStatus = True
    return writeStatus
      
  def verifyDimensions(self, inPixData):
    rowSizes = []
    dimensionsVerified = True
    for i in inPixData:
      rowSizes.append(i.__len__())
    for i in range(rowSizes.__len__() - 1):
      if rowSizes[i] != rowSizes[i+1]: 
	dimensionsVerified = False
	break
    debug("verify dimensions: " + str(dimensionsVerified))
    if dimensionsVerified == False:
      debug(rowSizes)
    return dimensionsVerified
  
    
  def clearPixData(self):
    self.pixelData = []

debug = True    
def debug(text):
  if debug: print("---debug: " + str(text))

