# Takes a string and makes individual images out of every word. Requires ImageMagick.
# Created 20150325
# By Jiseng So

theSentence = "Hello there, I am JisengSo. Lots of people think I'm a root. GINSENG_PLACEHOLDER I like video_games, music, video_game_music, and the occasional educational video. You will find all these kinds of videos and more, right here on my YouTube channel. Also, I like cheese!"

theWords = theSentence.split(" ")
outputPath = "baseImages"
filenameBase = "Intro_"
startNum = 0
curNum = startNum
filetype = "png"

background = "white"
fill = "black"
font = "Courier"
width = 5120
height = 2880
gravity = "center"


print "mkdir %s" % outputPath
for i in theWords:
  theWord = i.replace("_", " ")
  print "convert -background %s -fill %s -font %s -size %dx%d -gravity %s caption:\"%s\" %s/%s%07d.%s" % (background, fill, font, width, height, gravity, theWord, outputPath, filenameBase, curNum, filetype)
  curNum += 1








#convert -background white -fill black -font Courier -size 7680x4320 -gravity center caption:"foo\n\nThis is a very long thing of text to test some certain capabilities so that I can know stuff and do stuff and test stuff to know stuff." foo.png