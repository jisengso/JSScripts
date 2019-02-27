#!/bin/env python3

# WikiCalendar
# Pick a year and month, get a wikitext calendar.
# ./WikiCalendar.py 2018 3 # Create calendar for March 2018

# Future considerations:
#   Externalize configuration
import calendar
import sys
try:
    import holidays
except:
    print("holidays module not present. No holidays for you!", file=sys.stderr)

class Day:
    canHoliday = True
    try:
        USHolidays = holidays.US()
    except:
        canHoliday = False
    def __init__(self, dayStr="", doLink=False, doClass=False, year="", month="", dayClass=""):
        self.dayStr = dayStr
        self.doLink = doLink
        self.doClass = doClass
        self.year = year
        self.month = month
        self.dateStr = f"{year}{month}{dayStr}"
        self.dayClass = dayClass

    def __str__(self):
        PH = "{}"
        if self.dayStr == "":
            return "|"
        year = self.year
        month = self.month
        day = self.dayStr
        dateStr = self.dateStr
        result = f"| {PH}{day}"
        if self.doLink:
            result = f"| {PH}[[{dateStr}|{day}]]"

        if self.doClass:
            dayClass = self.dayClass
            weekday = calendar.weekday(int(year), int(month), int(day))
            if weekday in (calendar.SATURDAY, calendar.SUNDAY):
                dayClass += " weekend"
            elif dateStr in self.USHolidays:
                dayClass += " holiday"
            if dayClass:
                result = result.format(f"class=\"{dayClass.strip()}\" | ")
            else:
                result = result.format("")
        else:
            result = result.format("")
        return result

    def holidayItem(self):
        result = ""
        if self.canHoliday and self.year and self.month and self.dayStr:
            year = self.year
            month = self.month
            day = self.dayStr
            dateStr = self.dateStr

            if dateStr in Day.USHolidays:
                if self.doLink:
                    result = f"* [[{dateStr}|{day}]]: {Day.USHolidays.get(dateStr)}"
                else:
                    result = f"* {day}: {Day.USHolidays.get(dateStr)}"
        return result

class WikiCalendar:
    def __init__(self):
        self.yearNum = int(sys.argv[1])
        self.yearStr = str(self.yearNum)
        self.monthNum = int(sys.argv[2])
        self.monthStr = f"{self.monthNum:02}"
        self.holidayList = []
        self.calendarClass = "\"wikitable floatright\""
        self.placeHolder = "{}"
        self.doLinkTitle = True
        self.doLinkDays = True
        self.doDayClass = True
        self.doAdjacentMonths = True
        self.doAdjMonthDays = True
        self.doHolidayList = True
        self.nextMonthName = ""
        self.lastMonthName = ""
        self.prevMonth = ""
        self.nextMonth = ""

    def makeTitle(self):
        PH = self.placeHolder
        monthName = calendar.month_name[self.monthNum]
        titleList = []
        titleList.append(f"{{| class={self.calendarClass}")
        titleList.append(f"|+{PH}{monthName}{PH} {PH}{self.yearStr}{PH}")

        if self.doLinkTitle:
            preMonthLink = f"[[:category:{self.yearStr}{self.monthStr}|"
            postMonthLink = "]]"
            preYearLink = f"[[:category:{self.yearStr}|"
            postYearLink = "]]"
            titleList[1] = titleList[1].format(preMonthLink, postMonthLink, preYearLink, postYearLink)
        else:
            titleList[1] = titleList[1].format("", "", "", "")
        titleStr = "\n".join(titleList)

        return titleStr

    def makeHeader(self):
        PH = self.placeHolder
        headerList = ["|-"]
        for weekday in calendar.weekheader(3).split(" "):
            headerList.append(f"!{weekday}")
        headerStr = "\n".join(headerList)
        return headerStr

    def calcAdjMonths(self):
        if self.doAdjacentMonths or self.doAdjMonthDays:
            nextMonth = self.monthNum+1
            lastMonth = self.monthNum-1
            yearAdd = 0
            yearSub = 0

            if nextMonth == 13:
                nextMonth = 1
                yearAdd = 1
            self.nextMonthName = calendar.month_name[nextMonth]
            nextMonthStr = f"{nextMonth:02}"
            self.nextMonth = f"{self.yearNum+yearAdd}{nextMonthStr}"

            if lastMonth == 0:
                lastMonth = 12
                yearSub = -1
            self.lastMonthName = calendar.month_name[lastMonth]
            lastMonthStr = f"{lastMonth:02}"
            self.prevMonth = f"{self.yearNum+yearSub}{lastMonthStr}"

    def makeWeekLists(self):
        yearNum = self.yearNum
        monthNum = self.monthNum
        calendarList = calendar.monthcalendar(yearNum, monthNum)
        PH = self.placeHolder
        weekLists = []
        blankDay = Day()
        for week in calendarList:
            weekList = []
            for day in week:
                if day == 0:
                    weekList.append(blankDay)
                    continue
                dayStr = f"{day:02}"
                dayObj = ""
                if self.doLinkDays or self.doDayClass:
                    dayObj = Day(dayStr, self.doLinkDays, self.doDayClass, self.yearStr, self.monthStr)
                else:
                    dayObj = Day(dayStr)
                weekList.append(dayObj)
            weekLists.append(weekList)

        if self.doAdjMonthDays:
            weeks = (weekLists[0], weekLists[-1])
            years = (self.prevMonth[0:4], self.nextMonth[0:4])
            months = (self.prevMonth[4:6], self.nextMonth[4:6])
            prevMonthLastWeek = calendar.monthcalendar(int(years[0]), int(months[0]))[-1]
            nextMonthFirstWeek = calendar.monthcalendar(int(years[1]), int(months[1]))[0]
            calWeeks = (prevMonthLastWeek, nextMonthFirstWeek)

            for whichMonth, relWeek in enumerate(weeks):
                if blankDay in relWeek:
                    for weekday, day in enumerate(calWeeks[whichMonth]):
                        if day == 0:
                            continue
                        dayStr = f"{day:02}"
                        dayObj = ""
                        if self.doLinkDays or self.doDayClass:
                            dayObj = Day(dayStr, self.doLinkDays, self.doDayClass, years[whichMonth], f"{months[whichMonth]}", "diffMon")
                        else:
                            dayObj = Day(dayStr)
                        relWeek[weekday] = dayObj

        return weekLists


    def makeAdjMonths(self):
        outputList = []
        if self.doAdjacentMonths:

            outputList.append("|-")
            outputList.append(f"| colspan=3 | [[:category:{self.prevMonth}|{self.lastMonthName}]]")
            outputList.append(f"| colspan=4 style=\"text-align:right;\"| [[:category:{self.nextMonth}|{self.nextMonthName}]]")

        return outputList

    def makeHolidayList(self, weekLists):
        # Unfinished
        outputList = []
        for week in weekLists:
            for day in week:
                holidayItem = day.holidayItem()
                if holidayItem:
                    self.holidayList.append(holidayItem)

        if self.holidayList:
            outputList.append("|-")
            outputList.append("| colspan=7 | '''Holidays''':")
            outputList.append("\n".join(self.holidayList))

        return outputList


    def flattenWeekLists(self, weekLists):
        flatList = []
        for week in weekLists:
            tmpList = ["|-"]
            for day in week:
                tmpList.append(str(day))
            weekStr = "\n".join(tmpList)
            flatList.append(weekStr)
        return flatList


    def makeIt(self):

        title = self.makeTitle()
        header = self.makeHeader()
        self.calcAdjMonths()
        adjMonths = self.makeAdjMonths()
        weekLists = self.makeWeekLists()
        holidayList = self.makeHolidayList(weekLists)
        flatWeekList = self.flattenWeekLists(weekLists)

        print(title)
        for line in adjMonths:
            print(line)
        print(header)
        for week in flatWeekList:
            print(week)
        for line in holidayList:
            print(line)
        print("|}")


if __name__ == "__main__":
    newCalendar = WikiCalendar()
    newCalendar.makeIt()
