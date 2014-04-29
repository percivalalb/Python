'''
Created on 21 Nov 2013
@author: Alex
'''
import os
from PFSHandler import PFSBase
from PFSHandler import PFSTagInt
from PFSHandler import PFSTagString
from PFSHandler import PFSTagFloat
from PFSHandler import PFSTagCompound
from PFSHandler import PFSTagList
import Commands
from Commands import Command
from Commands import CommandHelp
import atexit
import _thread
import time

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

print("Starting alex's program v1.0.2a")
print("Loading save file")
saveFile = os.getcwd() + "\\mutitool.pfs"
fileBeingAccessed = False
fileData = PFSBase.readFromFile(saveFile)
print("Registering save handler")
atexit.register(programEnd, isThread = False, saveFileEvery = 1)
_thread.start_new_thread(programEnd, (True, 10))

print("For the list of commands type /help")
print("")

running = True

while running:
    
    userinput = input()

    command = Commands.getCommandFromName(userinput)
    
    if(command is not 0):
        args = userinput.split(' ')
        args.remove(command.getName(command))
        command.processCommand(command, args)

