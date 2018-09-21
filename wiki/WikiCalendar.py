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

nextMonth = monthNum+1
lastMonth = monthNum-1
addYear = 0
subYear = 0


if nextMonth == 13:
    nextMonth = 1
    addYear = 1
nextMonthName = calendar.month_name[nextMonth]
nextMonthStr = str(nextMonth)
if nextMonth < 10:
    nextMonthStr = "".join(["0", nextMonthStr])
if lastMonth == 0:
    lastMonth = 12
    subYear = -1
lastMonthName = calendar.month_name[lastMonth]
lastMonthStr = str(lastMonth)
if lastMonth < 10:
    lastMonthStr = "".join(["0", lastMonthStr])

calendarList = calendar.monthcalendar(yearNum, monthNum)
outputList = ["{| class=\"wikitable floatright\"",
              "".join(["|+[[:category:", yearStr, monthStr, " | ", calendar.month_name[monthNum], "]] [[:category:", yearStr, " | ", yearStr, "]]"]),
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

outputList.append("|-")
outputList.append("".join(["| colspan=3 | [[:category:", str(yearNum+subYear), lastMonthStr, " | ", lastMonthName, "]]"]))
outputList.append("".join(["| colspan=4 style=\"text-align:right;\"| [[:category:", str(yearNum+addYear), nextMonthStr, " | ", nextMonthName, "]]"]))
outputList.append("|}")

for line in outputList:
    print(line)
