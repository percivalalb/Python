'''
Created on 23 Apr 2014
@author: Alex
'''

class Command:

    def __init__(self):
        pass

    def getUsage(self):
        return ""

    def getName(self):
        return ""

    def processCommand(self, args):
        pass

class CommandHelp(Command):

    def getUsage(self):
        return "Lists all commands"

    def getName(self):
        return "/help"

    def processCommand(self, args):
        print("")
        for command in COMMANDS:
            print(command.getName(command) + ":", command.getUsage(command))
        print("")

class CommandHelp(Command):

    def getUsage(self):
        return "Lists all commands"

    def getName(self):
        return "/help"

    def processCommand(self, args):
        print("")
        for command in COMMANDS:
            print(command.getName(command) + ":", command.getUsage(command))
        print("")
        print(args)

COMMANDS = [CommandHelp]

def getCommandFromName(name):
    for command in COMMANDS:
        if name.startswith(command.getName(command)):
            return command
    return 0 
