# Relies on Imagemagick with "convert"

import sys
import subprocess
import os

mainCommand = "convert -background white -density 1200 +append"
SP = " "
LB = "["
RB = "]"
inputFilename = "driverguide-en.pdf"
outputParameters = "-flatten -background white"
outputPrefix = "image_"
numDigits = "%03d"
outputPostfix = ".png"
pagesPerImage = 2
noMorePages = "Requested FirstPage is greater than the number of pages in the file"

commandErrors = os.tmpfile()
commandOutput = os.tmpfile()
curPage = 0

errors = ""
output = ""

execString = mainCommand + SP

while errors == "":

        execString += inputFilename + LB + str(curPage) + RB + SP
        if curPage % pagesPerImage == pagesPerImage-1:
                execString += SP + outputParameters + SP + outputPrefix + numDigits % (curPage/pagesPerImage) + outputPostfix
                print execString
                subprocess.call(execString, stdout=commandOutput, stderr=commandErrors, shell=True)
                execString = mainCommand + SP
                commandErrors.seek(0)
                commandOutput.seek(0)
                errors = commandErrors.read().strip().replace("\r", "")
                output = commandOutput.read().strip().replace("\r", "")
        else:
                pass
        curPage +=1
print errors
print output