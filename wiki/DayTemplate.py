import calendar
import sys
import locale
locale.setlocale(locale.LC_ALL, "")

class DayTemplate:

	dayTemplate = """
== [[{year}{month:02}{day:02} | {weekday}, {day} {monthName} {year}]] ==

<noinclude>
{{{{{year}{month:02}}}}}
__TOC__
{{{{:{year}_Plan}}}}
</noinclude>

{{{{:{year}{month:02}_Plan}}}}
== Today's Plan ==
== Result ==
== Statistics ==
* Bottles of Soylent drunk: ?
* Weight: ? lbs
== Other ==

<noinclude>
[[category:{year}{month:02}]]
</noinclude>
"""

	def __init__(self, year, month, day):
		self.year = int(year)
		self.month = int(month)
		self.day = int(day)
		self.weekday = calendar.day_name[calendar.weekday(self.year, self.month, self.day)]
		self.monthName = calendar.month_name[self.month]

		self.contents = DayTemplate.dayTemplate.format(year=self.year, month=self.month, day=self.day, weekday=self.weekday, monthName=self.monthName)

	def print(self):
		print(self.contents)
	
if __name__ == "__main__":
	year = sys.argv[1]
	month = sys.argv[2]
	day = sys.argv[3]
	newDay = DayTemplate(year, month, day)
	newDay.print()