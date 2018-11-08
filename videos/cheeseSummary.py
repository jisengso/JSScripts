'''
cheeseSummary.py

Written by Jiseng So.

This script is meant to draw data from a tab-delimited list and create summaries. The primary summary is dreams/no-dreams per cheese type and various data derived from that. 

This will account for different field configurations by selecting particular fields by name. I may add different fields to track more data or someone else with different fields will use this script.

Mandatory fields are: date, cheeseType, hadDream, wasLucid

Summary types:

Main: cheeseType, trials, dreams, percentageDreams
allCheeseTrials, allCheeseDreams, allCheesePercentageDreams
noCheeseTrials, noCheeseDreams, noCheesePercentageDreams

Monthly: cheeseType, trials, dreams, percentageDreams
monthTrials, monthDreams, monthPercentageDreams

'''

import os
import sys
import math
import calendar

inFilename = "cheeseData.tsv"
outFilename = "cheeseSummary.tsv"
TB = "\t"
SP = " "
PC = "%"
NL = "\n"
inFile = open(inFilename, 'r')
outFile = open(outFilename, 'w')
rawData = []
debug = True

def processInFile(inputInFile, inputRawData):
  curLine = inputInFile.readline()
  while curLine != "":
    inputRawData.append(curLine.split(TB))
    curLine = inputInFile.readline()
    
def createMainSummary(inputRawData):
  summaryData = getFields(inputRawData, ["Date", "cheeseType", "hadDream", "wasLucid"])
  numTrials = summaryData.__len__()
  numDreams = 0
  numLucid = 0
  cheeseData = {}
# cheeseData is a dictionary. key is cheeseType. Data is number of trials and dreams.
  monthData = {}
# monthData is a dictionary. Key is the month. Data is array with number of trials and dreams, plus a dictionary with cheeseType as key with trials and dreams.  
  for i in summaryData:
    curDate = i[0]
    curCheeseType = i[1]
    curHadDream = i[2].__len__() == 4
    curWasLucid = i[3].__len__() == 4
    if not cheeseData.has_key(curCheeseType): 
      cheeseData[curCheeseType] = [0,0]
    curMonth = determineMonth(curDate)
    if not monthData.has_key(curMonth):
      monthData[curMonth] = [0, 0, {}]
    if not monthData[curMonth][2].has_key(curCheeseType):
      monthData[curMonth][2][curCheeseType] = [0, 0]
    cheeseData[curCheeseType][0] = cheeseData[curCheeseType][0] + 1
    monthData[curMonth][0] = monthData[curMonth][0] + 1
    monthData[curMonth][2][curCheeseType][0] = monthData[curMonth][2][curCheeseType][0] + 1
    if curHadDream:
      cheeseData[curCheeseType][1] = cheeseData[curCheeseType][1] + 1
      monthData[curMonth][1] = monthData[curMonth][1] + 1
      monthData[curMonth][2][curCheeseType][1] = monthData[curMonth][2][curCheeseType][1] + 1
      numDreams = numDreams + 1
    if curWasLucid:
      numLucid = numLucid + 1

  Output("Totals")
  Output("Trials" + TB + str(numTrials))
  Output("Dreams" + TB + str(numDreams))
  Output("dreamPercent" + TB + str(int((numDreams/(numTrials*1.))*100)) + PC)
  Output("")
  Output("cheeseType" + TB + "Trials" + TB + "Dreams" + TB + "dreamPercent")
  cheeseKeys = cheeseData.keys()
  cheeseKeys.sort()
  for i in cheeseKeys:
    curTrials = cheeseData[i][0]
    curDreams = cheeseData[i][1]
    Output (i + TB + str(curTrials) + TB + str(curDreams) + TB + str(int((curDreams/(curTrials*1.))*100)) + PC)
  Output(NL)
  Output("Month" + TB + "Trials" + TB + "Dreams" + TB + "dreamPercent")
  monthKeys = monthData.keys()
  monthKeys.sort()
  
  for i in monthKeys:
    curTrials = monthData[i][0]
    curDreams = monthData[i][1]
    monthCheeseData = monthData[i][2]
    Output(i + TB + str(curTrials) + TB + str(curDreams) + TB + str(int((curDreams/(curTrials*1.))*100)) + PC)
  Output("")

  for i in monthKeys:
    curTrials = monthData[i][0]
    curDreams = monthData[i][1]
    monthCheeseData = monthData[i][2]
    MCKeys = monthCheeseData.keys()
    MCKeys.sort()
    Output(i + TB + str(curTrials) + TB + str(curDreams) + TB + str(int((curDreams/(curTrials*1.))*100)) + PC)
    for j in MCKeys:
      MCTrials = monthCheeseData[j][0]
      MCDreams = monthCheeseData[j][1]
      Output (j + TB + str(MCTrials) + TB + str(MCDreams) + TB + str(int((MCDreams/(MCTrials*1.))*100)) + PC)
    Output("")

def determineMonth(dateValue):
  year = dateValue[0:4]
  month = dateValue[4:6]
  return year + SP + month

def getFields(inputRawData, desiredFieldsArray):
  relevantIndices = []
  processedData = []
  for i in desiredFieldsArray:
    for j in inputRawData[0]:
      if i == j.split(" ")[0]:
	relevantIndices.append(inputRawData[0].index(j))
	break
  for i in inputRawData:
    curLine = []
    for j in relevantIndices:
      curLine.append(i[j])
    if not curLine[0].__contains__("!") and not curLine[0].__contains__(desiredFieldsArray[0]):
      processedData.append(curLine)
  return processedData

def Debug(text):
  if debug: print (str(text))
def Output(text):
  outFile.write(text)
  print(text)
  
processInFile(inFile, rawData)
createMainSummary(rawData)