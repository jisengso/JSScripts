#!/usr/bin/env python3
"""
Short command to compress a bunch of video files. Takes a directory and compresses all video files within it.
Marks files compressed with this utility with metadata to prevent wasteful recompression.
Not recursive.
"""

import sys
import os
import time
from subprocess import Popen, PIPE

compressionCommandBase = "ffmpeg -i {} {} -metadata {} {}"
ffmpegCompressionSettings = "-c:a flac -compression_level 12 -c:v libvpx-vp9 -strict experimental -lossless 1 -threads 6 -frame-parallel 1 -row-mt 1 -tile-columns 2"
queryCommandBase = "mkvinfo {}"
metadataMarker = "COMPRESSED=VP9FLAC"
compressionPostfix = "VP9FLAC"
compressionTargetExtensions = ["mkv", "avi", "mp4"]
messages = []

fileList = os.listdir(sys.argv[1])
filesToCompress = []
for curFile in fileList:
    if curFile.split(".")[-1] in compressionTargetExtensions:
        filesToCompress.append(curFile)

for eachFile in filesToCompress:
    inputFile = f"\"{eachFile}\""
    queryCommand = queryCommandBase.format(inputFile)
    queryProcess = Popen(queryCommand, shell=True, stdout=PIPE)
    exitCode = queryProcess.wait()
    if compressionPostfix in str(queryProcess.stdout.read()):
        messages.append(f"{inputFile} skipped: Compression marker detected.")
        continue
    splittedName = eachFile.rsplit(".", 1)
    if len(splittedName) != 2:
        messages.append(f"{inputFile} skipped: Bad name.")
        continue
    baseName, extension = splittedName
    outputName = f"\"{baseName}.{compressionPostfix}.mkv\""
    if outputName.replace("\"", "") in fileList:
        messages.append(f"{inputFile} skipped: Output file exists.")
        continue
    compressionCommand = compressionCommandBase.format(inputFile, ffmpegCompressionSettings, metadataMarker, outputName)
    startTime = time.time()
    process = Popen(compressionCommand, shell=True)
    exitCode = process.wait()
    if exitCode != 0:
        messages.append(f"{inputFile}: Abnormal exit code {exitCode}.")
        continue
    endTime = time.time()
    secondsTaken = endTime-startTime
    messages.append(f"{inputFile}: {secondsTaken} seconds to compress.")


for message in messages:
    print(message)