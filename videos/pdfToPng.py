#!/usr/bin/env python3
"""
Converts a pdf into a series of images with pairs of pages.

Dependencies:
        'convert' from ImageMagick
        'pdfinfo'
"""

import sys
import subprocess
import tempfile
import math

mainCommand = "convert"
perInputArgs = "-density 600"
inputFilename = sys.argv[1]
outputParameters = "+append +repage -flatten -background white"
outputPrefix = "image_"
outputPostfix = ".png"
pagesPerImage = 2

commandErrors = tempfile.TemporaryFile()
commandOutput = tempfile.TemporaryFile()
curPage = 0

errors = b""
output = b""
pdfInfo = b""

subprocess.call(f"pdfinfo {inputFilename}", stdout=commandOutput, shell=True)
commandOutput.seek(0)
pdfInfo = commandOutput.read().strip().replace(b"\r", b"")
pagesLine = ""

for line in pdfInfo.split(b"\n"):
        if line.startswith(b"Pages:"):
                pagesLine = line
                break
totalPages = int(pagesLine.split()[1])
numDigits = f"%0{math.ceil(math.log(totalPages, 10))+1}d"

print(f"Reading {inputFilename}, which has {totalPages} pages.")

outputtedPages = set()

for curPage in range(totalPages):
        baseExec = f"{mainCommand} {perInputArgs} {inputFilename}[{curPage}]"
        outputFilename = f"{outputPrefix}{numDigits % (curPage/pagesPerImage)}{outputPostfix}"
        execString = ""
        if curPage % pagesPerImage == 0:
                execString = f"{baseExec} {perInputArgs} {inputFilename}[{curPage+1}] {outputParameters} {outputFilename}"
        elif curPage == totalPages-1 and outputFilename not in outputtedPages:
                execString = f"{baseExec} {outputParameters} {outputFilename}"

        if execString:
                print (execString)
                subprocess.call(execString, stdout=commandOutput, stderr=commandErrors, shell=True)
                commandErrors.seek(0)
                commandOutput.seek(0)
                errors = commandErrors.read().strip().replace(b"\r", b"")
                output = commandOutput.read().strip().replace(b"\r", b"")
                outputtedPages.add(outputFilename)

print (errors)
print (output)
