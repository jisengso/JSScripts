#!/usr/bin/env python3

import sys
import os
import struct
import subprocess

def debug(value, *args, **kwargs):
    print(value, *args, **kwargs)

class WavFile:
    def __init__(self):
        self.fileName = ""
        self.channels = 2
        self.samplerate = 48000
        self.samplesize = 2
        self.bytesPerSecond = self.channels * self.samplerate * self.samplesize
        self.audioData = b""
        self.blockAlign = self.channels * self.samplesize

    def openFile(self, filePath):
        debug(f"Opening {filePath}.")
        self.fileName = filePath
        theFile = open(filePath, 'rb')
        rawData = theFile.read(44)
        udTmp = struct.unpack('4sI4s4sIHHIIHH4sI', rawData)
        self.channels = udTmp[6]
        self.samplerate = udTmp[7]
        self.bytesPerSecond = udTmp[9]
        self.samplesize = udTmp[10]//8
        self.audioData = theFile.read()
        self.bytesPerSecond = self.channels * self.samplerate * self.samplesize
        self.blockAlign = self.channels * self.samplesize
        theFile.close()

    def saveFile(self, filePath):
        debug(f"Saving {filePath}.")
        self.fileName = filePath
        typicalWavHeaderSize = 36 # bytes
        theFile = open(filePath, "wb")
        totalSize = len(self.audioData)
        outputData = struct.pack("4sI4s4sIHHIIHH4sI", 
            b"RIFF", 
            typicalWavHeaderSize + totalSize, 
            b"WAVE", 
            b"fmt ", 
            16, 
            1, 
            self.channels, 
            self.samplerate, 
            self.bytesPerSecond, 
            self.channels*self.samplesize, 
            self.samplesize*8, 
            b"data", 
            totalSize)
        theFile.write(outputData)
        theFile.write(self.audioData)
        theFile.close()

    def matchSettings(self, otherWavFile):
        self.channels = otherWavFile.channels
        self.samplerate = otherWavFile.samplerate
        self.samplesize = otherWavFile.samplesize
        self.bytesPerSecond = otherWavFile.bytesPerSecond
        self.blockAlign = otherWavFile.blockAlign


class Deduper:
    def __init__(self, videoToDedupFilename):
        self.filename = videoToDedupFilename
        self.dedupedFilename = self.filename[:-4] + ".DEDUP.avi"
        self.infoFilename = self.filename + ".info"
        self.extractPath = ""
        self.dedupedAudioPath = ""
        self.outputFilename = ""
        self.fps = 60 # Maybe extract from info
        self.audioSlices = [] # Video frame numbers with desired audio slice.

    def dedupVideo(self):
        dedupCommand = f"ffmpeg -y -i '{self.filename}' -an -vf mpdecimate,showinfo,\"setpts=N\" -c:v ffv1 '{self.dedupedFilename}' 2> '{self.infoFilename}'"
        debug(dedupCommand)
        subprocess.call(dedupCommand, shell=True)

    def extractAudio(self, extractPath="/dev/shm/dedupTmp.wav"):
        self.extractPath = extractPath
        extractCommand = f"mpv '{self.filename}' -o='{extractPath}' --no-video"
        debug(extractCommand)
        subprocess.call(extractCommand, shell=True)
        # May want to detect error here.
    
    def loadFfmpegInfo(self):
        filename = self.infoFilename
        debug(f"Loading {self.infoFilename}")
        infoFile = open(filename, "rb")

        line = infoFile.readline()

        while line:
            ptsIndex = 0
            pts_timeIndex = 0
            try:
                ptsIndex = line.index(b"pts:")
                pts_timeIndex = line.index(b"pts_time:")
            
            except:
                line = infoFile.readline()

            if not ptsIndex:
                continue

            ptsValString = line[ptsIndex:pts_timeIndex].replace(b"pts:", b"").strip()
            ptsVal = int(ptsValString)
            self.audioSlices.append(ptsVal)
            line = infoFile.readline()

        infoFile.close()
        debug(f"Got {len(self.audioSlices)} frames.")

    def createDedupAudio(self, outputFilename="/dev/shm/deduped.wav"):
        debug(f"Deduplicating audio to {outputFilename}")
        self.dedupedAudioPath = outputFilename
        newWave = WavFile()
        origWave = WavFile()
        origWave.openFile(self.extractPath)
        newWave.matchSettings(origWave)
        audioFrameSize = origWave.bytesPerSecond // self.fps
        blockDiff = audioFrameSize % origWave.blockAlign
        audioFrameSizeAligned = audioFrameSize + blockDiff
        targetAccumulationBytes = 0
        accumulatedBytes = 0
        audioAccumulator = []

        for videoFrame in self.audioSlices:
            beginByteIndex = audioFrameSize * videoFrame
            beginByteIndex += beginByteIndex % origWave.blockAlign
            endByteIndex = audioFrameSize * (videoFrame + 1)
            endByteIndex += beginByteIndex % origWave.blockAlign

            audioAccumulator.append(origWave.audioData[beginByteIndex:endByteIndex])

            targetAccumulationBytes += audioFrameSize
            accumulatedBytes += endByteIndex - beginByteIndex
        
        newWave.audioData = b"".join(audioAccumulator)
        newWave.saveFile(outputFilename)

        debug("Desired accumulated bytes:", targetAccumulationBytes)
        debug("Output audio bytes:", accumulatedBytes)

    def muxMkv(self, outputFilename=""):
        if not outputFilename:
            self.outputFilename = self.filename[:-4] + ".DEDUP.mkv"
        else:
            self.outputFilename = outputFilename
        muxCommand = f"mkvmerge -o {self.outputFilename} {self.dedupedFilename} {self.dedupedAudioPath}"
        debug(muxCommand)
        subprocess.call(muxCommand, shell=True)

    def deleteTmpFiles(self):
        os.unlink(self.dedupedFilename)
        os.unlink(self.infoFilename)
        os.unlink(self.extractPath)
        os.unlink(self.dedupedAudioPath)

if __name__ == "__main__":
    videoFilename = sys.argv[1]
    deduperInstance = Deduper(videoFilename)
    deduperInstance.dedupVideo()
    deduperInstance.extractAudio()
    deduperInstance.loadFfmpegInfo()
    deduperInstance.createDedupAudio()
    deduperInstance.muxMkv()
    deduperInstance.deleteTmpFiles()