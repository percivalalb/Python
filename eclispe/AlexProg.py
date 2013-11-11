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

fileData = PFSTagCompound("")

@atexit.register
def programEnd():
    print "--Saving file..."
    global fileData
    fileData.addTag(PFSTagCompound("Compound test").addTag(PFSTagInt("ran").setValue(2)).addTag(PFSTagInt("daweran").setValue(32)))
    fileData.addTag(PFSTagInt("ran").setValue(2))
    fileData.addTag(PFSTagInt("dawe").setValue(3))
    fileData.addTag(PFSTagInt("ran").setValue(3132))
    fileData.addTag(PFSTagList("ran").appendTag(PFSTagInt("testlist2").setValue(699)).appendTag(PFSTagInt("testlist").setValue(69)))
    fileData.printValues(0)
    PFSBase.writeToFile(currentDirectory + "\\test.txt", fileData)
    print "--Finished saving file..."

currentDirectory = os.getcwd()

print "--Loading save file..."
data = PFSBase.readFromFile(currentDirectory + "\\test.txt")
data.printValues(0)
print "--Finished loading save file..."

hi = raw_input()

fileData.addTag(PFSTagString("input").setValue(hi))

