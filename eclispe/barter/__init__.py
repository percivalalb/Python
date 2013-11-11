'''
Created on 8 Nov 2013
@author: Alex
'''
import os
from barter.psf.PFSHandler import PFSBase
from barter.psf.PFSHandler import PFSTagInt
from barter.psf.PFSHandler import PFSTagString
from barter.psf.PFSHandler import PFSTagFloat
from barter.psf.PFSHandler import PFSTagCompound
from barter.psf.PFSHandler import PFSTagList


currentDirectory = os.getcwd()

data = PFSBase.readFromFile(currentDirectory + "\\test.txt")
data.printValues(0)

newData = PFSTagCompound("Test")
newData.addTag(PFSTagCompound("Compound test").addTag(PFSTagInt("ran").setValue(2)).addTag(PFSTagInt("daweran").setValue(32)))
newData.addTag(PFSTagInt("ran").setValue(2))
newData.addTag(PFSTagInt("dawe").setValue(3))
newData.addTag(PFSTagInt("ran").setValue(3132))
newData.addTag(PFSTagList("ran").appendTag(PFSTagInt("testlist2").setValue(699)).appendTag(PFSTagInt("testlist").setValue(69)))
hi = raw_input()

newData.addTag(PFSTagString("input").setValue(hi))

PFSBase.writeToFile(currentDirectory + "\\test.txt", newData)

