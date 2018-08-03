#!/usr/bin/python
# This script puts dates on the images and outputs them as BMP through ImageMagick.
# I might be eating the cheese some time past midnight, so shift back twelve hours.

import EXIF

def getJpegDate(theFileName):
  theFile = open(theFileName, 'r')
  DTG = EXIF.process_file(theFile)["Image DateTime"].printable
  year = DTG[0:4]
  month = DTG[5:7]
  day = DTG[8:10]
  hour = DTG[11:13]
  
  return int(year), int(month), int(day), int(hour)


