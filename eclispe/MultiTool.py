'''
Created on 21 Nov 2013
@author: Alex
'''

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

saveFile = os.getcwd() + "\\mutitool.pfs"
fileBeingAccessed = False
fileData = PFSBase.readFromFile(saveFile)

def programEnd(isThread, saveFileEvery):
    count = 0
    while isThread or count <= 0:
        count += 1
        global fileBeingAccessed
        global fileData
        
        if isThread or fileBeingAccessed:
            time.sleep(saveFileEvery)
        
        fileBeingAccessed = True
        PFSBase.writeToFile(saveFile, fileData)
        fileBeingAccessed = False

atexit.register(programEnd, isThread = False, saveFileEvery = 1)
thread.start_new_thread(programEnd, (True, 10))

print "[] Welcome to MultiTool []"

running = True

while running:
    print "Current tools are..."
    print "/printsavefile"
    
    input = raw_input()
    print ""
    if input.lower() == "/printsavefile":
        fileData.printValues(1)
    
    
    print ""

