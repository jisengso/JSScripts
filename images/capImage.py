
from PIL import ImageGrab, Image
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

'''
The purpose of this program is to provide high quality image captures. This can be preferable to using a screen recorder where maximizing image quality is the priority, since screen recorders will often use lossy compression codecs such as H264, VP9, Opus, MPEG, and many others. Screen recorders will also record audio and synchronize them with the resulting video. This program aims only to capture images and will not record audio.

By default, this program will capture the contents of the primary screen in PNG, which is lossless, at 1 frame per second. Impact on performance should be minimal, depending on screen size and complexity of the image. Ensure that there is enough space to store the resulting images! Additional compression of the resulting PNGs can further reduce space usage.

A few deduplication methods are available. By default, the program will not save the exact same image twice in the same session.

Example use cases:
	Screenshots of games
	Demonstration of how to perform an action

'''

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

counter = 0
captureDir = ""

# captureMethod 0: PIL capturing main screen
captureMethod = 0

windowName = "Fallout3"
followFocus = True


# dedupMethod 0: Consecutive deduplication. Does not save consecutive exact same images.
# dedupMethod 1: Consecutive N deduplication. Does not save if duplicated within the last N screenshots. N = dedupLastNum
# dedupMethod 2: Session deduplication. Never save exact same image in same session.
dedupMethod = 2

dedupLastNum = 30

curImage = -404
curImageHash = -404
prevImageHash = -404

hashCache = []

global exitNext
exitNext = -404

def dupImage():
	print (time.ctime() + ": Duplicate image detected. Not saving this one.")
def signal_handler(signalNum, frame):
	print (time.ctime() + ": Termination signal received: " + signalNum.__str__() + ", " + frame.__str__())
	global exitNext
	exitNext = 200
	
signal.signal(signal.SIGINT, signal_handler)
	
if 1:
	dirList = []
	tmpList = os.listdir(".")
	for i in tmpList:
		if stat.S_ISDIR(os.stat(i).st_mode):
			dirList.append(i)
	dirCount = dirList.__len__()
	captureDir = "capture%03d"%(dirCount + 1) + "/"
	os.mkdir(captureDir + "/")
	
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
	
	if curImage == -404:
		pass
		
	elif dedupMethod==0:
		if curImageHash != prevImageHash:
			print (time.ctime() + ": Saving " + captureDir + "screen_capture%06d.png"%counter)
			curImage.save(captureDir + "screen_capture%06d.png"%counter, "PNG")
			counter += 1
			prevImageHash = curImageHash
		else: dupImage()
		
	elif dedupMethod==1:
		if not hashCache.__contains__(curImageHash):
			hashCache.append(curImageHash)
			print (time.ctime() + ": Saving " + captureDir + "screen_capture%06d.png"%counter)
			curImage.save(captureDir + "screen_capture%06d.png"%counter, "PNG")
			counter += 1
			if hashCache.__len__() > dedupLastNum:
				hashCache.remove(0)
		else: dupImage()
		
	elif dedupMethod==2:
		if not hashCache.__contains__(curImageHash):
			hashCache.append(curImageHash)
			print (time.ctime() + ": Saving " + captureDir + "screen_capture%06d.png"%counter)
			curImage.save(captureDir + "screen_capture%06d.png"%counter, "PNG")
			counter += 1
		else: dupImage()
	else:
		print("Invalid deduplication method. ")
		break
		

print (time.ctime() + ": Exiting.")
sys.exit(0)
