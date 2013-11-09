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

currentDirectory = os.getcwd()

print "--Loading save file..."
data = PFSBase.readFromFile(currentDirectory + "\\test.txt")
data.printValues(0)
print "--Finished loading save file..."

newData = PFSTagCompound("Test")
newData.addTag(PFSTagCompound("Compound test").addTag(PFSTagInt("ran").setValue(2)).addTag(PFSTagInt("daweran").setValue(32)))
newData.addTag(PFSTagInt("ran").setValue(2))
newData.addTag(PFSTagInt("dawe").setValue(3))
newData.addTag(PFSTagInt("ran").setValue(3132))
newData.addTag(PFSTagList("ran").appendTag(PFSTagInt("testlist2").setValue(699)).appendTag(PFSTagInt("testlist").setValue(69)).removeTag("testlist"))
hi = raw_input()

newData.addTag(PFSTagString("input").setValue(hi))

PFSBase.writeToFile(currentDirectory + "\\test.txt", newData)

