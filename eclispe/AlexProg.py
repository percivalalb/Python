'''
Created on 9 Nov 2013
@author: Alex
'''

import os
from PFSHandler import PFSBase
from PFSHandler import PFSTagInt
from PFSHandler import PFSTagString
from PFSHandler import PFSTagFloat
from PFSHandler import PFSTagCompound
from PFSHandler import PFSTagList
import atexit
import thread
import time

fileData = PFSTagCompound("")
currentDirectory = os.getcwd()
fileBeingAccessed = False

def programEnd(isThread, saveFileEvery):
    global fileBeingAccessed
    global fileData
    
    if isThread or fileBeingAccessed:
        time.sleep(saveFileEvery)
    
    print "--Saving file..."
    fileData.printValues(0)
    fileBeingAccessed = True
    PFSBase.writeToFile(currentDirectory + "\\test.txt", fileData)
    fileBeingAccessed = False
    print "--Finished saving file..."

atexit.register(programEnd, isThread = False, saveFileEvery = 1)
thread.start_new_thread(programEnd, (True, 5))

print "--Loading save file..."
fileBeingAccessed = True
data = PFSBase.readFromFile(currentDirectory + "\\test.txt")
fileBeingAccessed = False
data.printValues(0)
print "--Finished loading save file..."

hi = raw_input()

fileData.addTag(PFSTagString("input").setValue(hi))
fileData.addTag(PFSTagCompound("Compound test").addTag(PFSTagInt("ran").setValue(2)).addTag(PFSTagInt("daweran").setValue(32)))
fileData.addTag(PFSTagInt("ran").setValue(2))
fileData.addTag(PFSTagInt("dawe").setValue(3))
fileData.addTag(PFSTagInt("ran").setValue(3132))
fileData.addTag(PFSTagList("ran").appendTag(PFSTagInt("testlist2").setValue(699)).appendTag(PFSTagInt("testlist").setValue(69)))

