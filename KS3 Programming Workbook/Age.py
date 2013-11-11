'''
Created on 9 Nov 2013
@author: Alex
'''

from datetime import datetime

#Value of the month to its name
def getMonthName(index):
    if index < 1:
        return "Too Small"
    elif index > 12:
        return "Too Big"
    
    return names[index - 1] 

def getDateEnding(index):
    return dateEnding[index - 1]

def getDaysInMonth(index):
    if index == 2:
        return daysInMonth[index - 1] - 1
    return daysInMonth[index - 1]

#Lists
names = ["January", "Feburary", "March", "April",
         "May", "June", "July", "August", "September",
         "October", "November", "December"]

dateEnding = ["st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th", "st"]

daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def timeEnding(obj):
    if len(str(obj)) < 2:
        return "0" + str(obj)
    return str(obj)


#Values of when you were born
YEAR = 1999
MONTH = 7
DAY = 13
CURRENT_YEAR = datetime.now().year
CURRENT_MONTH = datetime.now().month
CURRENT_DAY = datetime.now().day

daysAlive = 0

for i in range(MONTH, 12):
    for j in range(DAY, daysInMonth[i]):
        daysAlive += 1
        
print daysAlive

