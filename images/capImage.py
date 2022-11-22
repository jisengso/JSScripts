'''
The purpose of this program is to provide high quality image captures. This can be preferable to using a screen recorder where maximizing image quality is the priority, since screen recorders will often use lossy compression codecs such as H264, VP9, Opus, MPEG, and many others. Screen recorders will also record audio and synchronize them with the resulting video. This program aims only to capture images and will not record audio.

By default, this program will capture the contents of the primary screen in PNG, which is lossless, at 1 frame per second. Impact on performance should be minimal, depending on screen size and complexity of the image. Ensure that there is enough space to store the resulting images! Additional compression of the resulting PNGs can further reduce space usage.

A few deduplication methods are available. By default, the program will not save the exact same image twice in the same session.

Example use cases:
	Screenshots of games
	Demonstration of how to perform an action

'''

try:
	from PIL import ImageGrab, Image
except:
	print("Cannot import Python Imaging Library.")
	exit(-1)

import multiprocessing
from multiprocessing import Pool
import time
import os
import stat
import signal
import sys
import struct
try:
	from cStringIO import StringIO
except:
	from io import StringIO


#Bugs:

# Doesn't capture from all fullscreen games (example: FF8 for PC)

#Features to add:
#
# Screen selection
# Tie to window or process
# External configuration
# 	Capture rate
#	Capture directories - main, sub
#	Naming conventions
#	File format
#	Capture cursor
# Linux compatibility
# Possible multiprocessing
# Hash-based deduplication
#	Write a hash file upon termination?

def dupImage():
	print (time.ctime() + ": Duplicate image detected. Not saving this one.")
def signal_handler(signalNum, frame):
	print (time.ctime() + ": Termination signal received: " + signalNum.__str__() + ", " + frame.__str__())
	global exitNext
	exitNext = 200

def childSigHandler(signalNum, frame):
	print (time.ctime() + ": Child received termination signal: " + signalNum.__str__() + ", " + frame.__str__())
	global exitNext
	exitNext = 200

def saveImage(*args, **kwds):
	signal.signal(signal.SIGINT, signal.SIG_IGN)
	imageFromPIL, saveFileName = args
	print (time.ctime() + ": Saving " + saveFileName)
	imageFromPIL.save(saveFileName, "PNG", optimize=False, compress_level=1)

if __name__ == "__main__":
	multiprocessing.freeze_support()

	counter = 0
	captureDir = ""

	# captureMethod 0: PIL capturing main screen
	# There used to be two capture methods.
	captureMethod = 0

	filePrefix = f"capture"
	if len(sys.argv) > 1:
		filePrefix = sys.argv[1]

	curDate = time.localtime()
	dateStamp = f"{curDate.tm_year:04}{curDate.tm_mon:02}{curDate.tm_mday:02}"
	dateStr = f"{dateStamp}-{curDate.tm_hour:02}{curDate.tm_min:02}{curDate.tm_sec:02}"
	dirName = f"{filePrefix}-{dateStr}"
	username = os.getlogin()
	username = username.replace(" ", "_")

	# dedupMethod 0: Consecutive deduplication. Does not save consecutive exact same images.
	# dedupMethod 1: Session deduplication. Never save exact same image in same session.
	dedupMethod = 1

	dedupLastNum = 30

	# savingProcesses: number of processes to save with.
	savingProcesses = 5

	curImage = -404
	curImageHash = -404
	prevImageHash = -404

	hashCache = set()

	global exitNext
	exitNext = -404


	signal.signal(signal.SIGINT, signal_handler)

	dirList = []
	tmpList = os.listdir(".")
	for i in tmpList:
		if stat.S_ISDIR(os.stat(i).st_mode):
			dirList.append(i)
	dirCount = dirList.__len__()
	captureDir = dirName
	os.mkdir(captureDir + "/")


	savingPool = Pool(savingProcesses)

	while exitNext == -404:

		try:
			time.sleep(1)
		except:
			pass

		try:
			if captureMethod == 0:
				curImage = ImageGrab.grab()
			curImageHash = hash(curImage.tobytes())
		except:
			print (time.ctime() + ": Image capture fail: ", sys.exc_info()[0])
			curImage = -404
			curImageHash = -404

		filename = os.path.join(captureDir, f"{dateStr}_{filePrefix}_{username}_{counter:010}.png")
		saveImageArgs = (curImage, filename)

		if curImage == -404:
			pass

		elif dedupMethod==0:
			if curImageHash != prevImageHash:
				result = savingPool.apply_async(saveImage, saveImageArgs)
				counter += 1
				result.get()
				prevImageHash = curImageHash
			else: dupImage()

		elif dedupMethod==1:
			if curImageHash not in hashCache:
				hashCache.add(curImageHash)
				result = savingPool.apply_async(saveImage, saveImageArgs)
				result.get()
				counter += 1
			else: dupImage()
		else:
			print("Invalid deduplication method. ")
			break

	savingPool.close()
	time.sleep(1)
	savingPool.join()
	print (time.ctime() + ": Exiting.")
	exit(0)
