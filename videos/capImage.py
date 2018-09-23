
from PIL import ImageGrab, Image
import time
import os
import stat
import signal
import sys
import struct
import win32gui, win32ui, win32con, win32api
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
# captureMethod 1: win32api
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
def win32apiImageGrab():
	hwin = -404
	if followFocus:
		hwin = win32gui.GetForegroundWindow()
	else:
		hwin = win32gui.FindWindow(None, windowName)
	print time.ctime() + ": " + win32gui.GetWindowText(win32gui.GetForegroundWindow())
#	winPlacement = win32gui.GetWindowPlacement(hwin)
#	left = winPlacement[4][0]
#	top = winPlacement[4][1]
	
	left, top, right, bottom = win32gui.GetWindowRect(hwin)
#	width = right - left
#	height = top - bottom
	junk1, junk2, width, height = win32gui.GetClientRect(hwin)
	
#	print left, top, right, bottom
	
	hwindc = win32gui.GetWindowDC(hwin)
	srcdc = win32ui.CreateDCFromHandle(hwindc)
	memdc = srcdc.CreateCompatibleDC()
	bmp = win32ui.CreateBitmap()
	bmp.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(bmp)
	memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)
	bmpTuple = bmp.GetBitmapBits()
	srcdc.DeleteDC()
	memdc.DeleteDC()
	win32gui.ReleaseDC(hwin, hwindc)
	win32gui.DeleteObject(bmp.GetHandle())

	bmpBytes = StringIO()

	count = 0
	tmpList = []
	for i in bmpTuple:
		if count % 4 == 3:
			bmpBytes.write(struct.pack("bbbB", tmpList[0], tmpList[1], tmpList[2], 255))
			tmpList = []
		else:
			tmpList.insert(0, i)
		count+=1

	curImage = Image.frombytes("RGBA", (width, height), bmpBytes.getvalue())
	
	return curImage
	
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
		elif captureMethod == 1:
			curImage = win32apiImageGrab()
		curImageHash = hash(curImage.tobytes())
	except:
		print time.ctime() + ": Image capture fail: ", sys.exc_info()[0]
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
