'''
Created on 9 Nov 2013
@author: Alex
'''

from datetime import datetime

#Value of the month to its name
def getMonthName(monthIndex):
    assert (monthIndex >= 1 and monthIndex <= 12), "Outside the valid month index"
    return names[monthIndex - 1] 

def getDateEnding(dayIndex):
    assert (dayIndex >= 1 and dayIndex <= 31), "Outside the valid day index"
    return dateEnding[dayIndex - 1]

def getDaysInMonth(index,leapYear=False):
    assert (index >= 1 and index <= 12), "Outside the valid month index"
    if index == 2 and leapYear:
        return daysInMonth[index - 1] + 1
    return daysInMonth[index - 1]

def isLeapYear(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False

#Lists
names = ["January", "February", "March", "April", "May", "June", "July", "August", "September","October", "November", "December"]
dateEnding = ["st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", "st"]
daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def timeEnding(obj):
    if len(str(obj)) < 2:
        return "0" + str(obj)
    return str(obj)


#Values of when you were born
YEAR = int(raw_input("Please give the year you were born: "))
MONTH = int(raw_input("Please give the month you were born: "))
DAY = int(raw_input("Please give the day you were born: "))

CURRENT_YEAR = datetime.now().year
CURRENT_MONTH = datetime.now().month
CURRENT_DAY = datetime.now().day

totalDays = 0
newYearDays = 0
christmasDays = 0
leapDays = 0
    
for y in range(YEAR, CURRENT_YEAR + 1):
    
    'Initisalise the variables for the days in the current iteration for this year'
    startMonth = 1
    endMonth = 12
    if y == YEAR:
        startMonth = MONTH
    if y == CURRENT_YEAR:
        endMonth = CURRENT_MONTH
        
    for m in range(startMonth, endMonth + 1):
        
        startDay = 1
        endDay = getDaysInMonth(m, isLeapYear(y))
        if y == YEAR and m == MONTH:
            startDay = DAY
        if y == CURRENT_YEAR and m == CURRENT_MONTH:
            endDay = CURRENT_DAY - 1
            
        for d in range(startDay, endDay + 1):
            totalDays += 1
            if m == 1 and d == 1:
                newYearDays += 1
            if m == 12 and d == 25:
                christmasDays += 1
            if m == 2 and d == 29:
                leapDays += 1
            
            # print str(d) + getDateEnding(d), getMonthName(m), y
        
print "Some data about how many days you have lived..."
print "  Total Days:", totalDays
print "  New Year Days:", newYearDays
print "  Christmas Days:", christmasDays
print "  Leap Days:", leapDays