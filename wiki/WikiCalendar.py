#!/bin/env python3

# WikiCalendar
# Pick a year and month, get a wikitext calendar.
# ./WikiCalendar.py 2018 3 # Create calendar for March 2018

import calendar
import sys

yearNum = int(sys.argv[1])
yearStr = str(yearNum)
monthNum = int(sys.argv[2])
monthStr = str(monthNum)
if monthNum < 10:
    monthStr = "".join(["0", monthStr])

calendarList = calendar.monthcalendar(yearNum, monthNum)
outputList = ["{| class=\"wikitable floatright\"",
              "".join(["|+", calendar.month_name[monthNum]]),
              "|-"]

for weekday in calendar.weekheader(3).split(" "):
    outputList.append("".join(["!", weekday]))

for week in calendarList:
    outputList.append("|-")
    for day in week:
        dayStr = str(day)
        if day == 0:
            outputList.append("|")
            continue
        if day < 10:
            dayStr = "".join(["0", dayStr])
        outputList.append("".join(["| [[", yearStr, monthStr, dayStr, " | ", dayStr, "]]"]))

outputList.append("|}")

for line in outputList:
    print(line)
