# Converts time indexes to Python lists for frame numbers. This is so that I can manually write time indexes and have frame numbers calculated automatically for arbitrary fps without getting a headache.
# Created 20150325
# By Jiseng So

timeIndex = "0:00:00.000	Hello\n0:00:00.326	there\n0:00:00.640	I\n0:00:00.815	am\n0:00:00.964	Jiseng So\n0:00:01.535	Lots\n0:00:01.747 of\n0:00:01.861	people\n0:00:02.063	think\n0:00:02.260 I'm\n0:00:02.442	a\n0:00:02.500 root\n0:00:02.870 GINSENG PLACEHOLDER\n0:00:02.925	I\n0:00:03.092 like\n0:00:03.250 video games\n0:00:04.006	music\n0:00:04.603 video game music\n0:00:05.713	and\n0:00:05.794 the\n0:00:05.914	occasional\n0:00:06.448 educational\n0:00:07.099	video\n0:00:07.682 You\n0:00:07.811	will\n0:00:07.904 find\n0:00:08.276 all\n0:00:08.440	these\n0:00:08.648 kinds\n0:00:08.833	of\n0:00:08.946	videos\n0:00:09.275 and\n0:00:09.420 more\n0:00:09.763 right\n0:00:09.954 here\n0:00:10.164 on\n0:00:10.264 my\n0:00:10.413 YouTube\n0:00:10.726 channel\n0:00:11.136 also\n0:00:11.482 I\n0:00:11.599 like\n0:00:11.757 CHEEEEEEEEESE!\n0:00:21.846 end"

fps = 60

#precision indicates either by seconds, milliseconds, or microseconds
#0 seconds
#1 milliseconds
#2 microseconds
precision = 1

framePositionList = []
outputList = []

timeEntries = timeIndex.split("\n")
for i in timeEntries:
  hours = int(i[0])
  minutes = int(i[2:4])
  seconds = int(i[5:7])
  milliseconds = 0.
  microseconds = 0.
  if precision > 0:
    milliseconds = float(i[8:11])
    if precision > 1:
      microseconds = float(i[11:14])
  framePosition = fps * (hours*(60*60) + minutes*60 + seconds)
  framePosition += (fps * milliseconds) / 1000
  framePosition += (fps * microseconds) / 1000000
  framePosition = int(framePosition)
  framePositionList.append(framePosition)

for i in xrange(framePositionList.__len__() - 1):
  outputList.append(framePositionList[i+1] - framePositionList[i])

print (outputList)