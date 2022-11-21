#!/usr/bin/env python3

"""
Calculates time offsets using the earliest time as the base time. 
Good for time-sequenced things, such as videos and audio.

Takes input from stdin that looks like this:

2022-11-19 22-40-07
2022-11-19 23-18-57
2022-11-19 23-20-52
2022-11-19 23-44-31
2022-11-19_22-30-42
2022-11-19_22-58-05
2022-11-19_23-38-45
2022-11-19_23-46-12
2022-11-19_23-46-49

"""

from datetime import *
import sys

def secondsToTime(inSeconds):
    hours = inSeconds//3600
    minutes = (inSeconds//60) % 60
    seconds = inSeconds % 60

    outString = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    return outString

inputList = []

for line in sys.stdin:
    inputList.append(line)

datetimeList = []

for inputDate in inputList:
    normalized = inputDate.replace(" ", "-")
    normalized = normalized.replace("_", "-")
    normalized = normalized.replace("\n", "")
    normalized = normalized.replace("\r", "")
    components = normalized.split("-")

    integerizedComponents = []

    for component in components:
        try:
            integerizedComponents.append(int(component))
        except:
            pass
    if integerizedComponents:
        datetimeList.append((normalized, (datetime(*integerizedComponents))))

datetimeList.sort()

basedatetime = datetimeList[0]
print(basedatetime[0], "00:00:00")


for eachTime in datetimeList[1:-1]:
    difference = eachTime[1] - basedatetime[1]
    formattedDifference = secondsToTime(difference.seconds)
    print(eachTime[0], formattedDifference)