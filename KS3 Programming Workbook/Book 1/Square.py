'''
Created on 9 Nov 2013
@author: Alex
'''

import sys

length = raw_input("What is the length of your room in metres? ")

try:
    lengthInt = float(length)
except ValueError:
    print "Error: Please only enter numbers!"
    sys.exit(128)

width = raw_input("What is the width of your room in metres? ")

try:
    widthInt = float(width)
except ValueError:
    print "Error: Please only enter numbers!"
    sys.exit(128)
    
print "You need " + str(widthInt * lengthInt) + "m squared of material."