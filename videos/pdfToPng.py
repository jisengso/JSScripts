#!/usr/bin/env python3

"""
Converts a pdf into a series of images with pairs of pages.

Relies on Imagemagick with "convert"

Future capabilities to consider:
* Consider pdfs with odd numbers of pages
* Get number of pages before actually processing
"""
import sys
import subprocess
import tempfile

mainCommand = "convert"
SP = " "
LB = "["
RB = "]"
perInputArgs = "-density 600"
inputFilename = sys.argv[1]
outputParameters = "+append +repage -flatten -background white"
outputPrefix = "image_"
numDigits = "%03d"
outputPostfix = ".png"
pagesPerImage = 2
noMorePages = "Requested FirstPage is greater than the number of pages in the file"

commandErrors = tempfile.TemporaryFile()
commandOutput = tempfile.TemporaryFile()
curPage = 0

errors = b""
output = b""

execString = mainCommand + SP

while errors == b"":

        execString += SP + perInputArgs + SP + inputFilename + LB + str(curPage) + RB + SP
        if curPage % pagesPerImage == pagesPerImage-1:
                execString += SP + outputParameters + SP + outputPrefix + numDigits % (curPage/pagesPerImage) + outputPostfix
                print (execString)
                subprocess.call(execString, stdout=commandOutput, stderr=commandErrors, shell=True)
                execString = mainCommand + SP
                commandErrors.seek(0)
                commandOutput.seek(0)
                errors = commandErrors.read().strip().replace(b"\r", b"")
                output = commandOutput.read().strip().replace(b"\r", b"")
        else:
                pass
        curPage +=1
print (errors)
print (output)
