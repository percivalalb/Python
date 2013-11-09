'''
Created on 8 Nov 2013
@author: Alex
'''
import os

class PFSBase:
    
    MAPPING = ['NULL', 'INT', 'STRING', 'FLOAT', 'LONG', 'LIST', 'COMPOUND']
    
    def __init__(self):
        self.tagName = ""
        self.type = 0
        self.value = 0

    def write(self, fob):
        nameLength = str(len(str(self.tagName)))
        valueLength = str(len(str(self.value)))
        text = "%d%s:%s:%s%s" % (self.type, nameLength, valueLength, self.tagName, self.value)
        fob.write(text)

    def read(self, fob, nameSize, valueSize):
        return
    
    def printValues(self, indent):
        realIndent = ""
        for i in range(indent):
            realIndent += "   "
        
        print realIndent + self.tagName, ":", self.value
        return
    
    def setValue(self, value):
        self.value = value
        return self

    @staticmethod
    def getTypeFromId(id):
        if id == 0:
            return 0
        elif id == 1:
            return PFSTagInt("")
        elif id == 2:
            return PFSTagString("")
        elif id == 3:
            return PFSTagFloat("")
        elif id == 4:
            return PFSTagLong("")
        elif id == 5:
            return PFSTagList("")
        elif id == 6:
            return PFSTagCompound("")
        return 0

    @staticmethod
    def readFromFile(fileLoc):
        'Creates a new file if none exits'
        open(fileLoc, 'a').close()
        fob = open(fileLoc, 'r+')
        fileSize = int(os.path.getsize(fileLoc))
        data = []
        while fileSize > fob.tell():
            id = int(fob.read(1))
            charFound = 0;
            nameSize = ""
            valueSize = ""
            
            while charFound < 2:
                lastChar = fob.read(1)
                if(lastChar == ":"):
                    charFound = charFound + 1
                elif(charFound == 0):
                    nameSize = nameSize + lastChar 
                elif(charFound == 1):
                    valueSize = valueSize + lastChar  
            
                    
            nameSize = int(nameSize)
            valueSize = int(valueSize)  
            type = PFSBase.getTypeFromId(id)
            type.read(fob, nameSize, valueSize)
            data.append(type)
            
        fob.close()
        tagCompound = PFSTagCompound("")
        tagCompound.value = data
        return tagCompound

    @staticmethod
    def writeToFile(fileLoc, tagCompound):
        fob = open(fileLoc, 'w+')
        for tag in tagCompound.value:
            tag.write(fob)
        fob.close()
        
class PFSTagFloat(PFSBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 3
        self.value = 0.0

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = float(fob.read(valueSize))
        self.value = value
        
class PFSTagInt(PFSBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 1
        self.value = 0

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = int(fob.read(valueSize))
        self.value = value
        
class PFSTagLong(PFSBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 4
        self.value = 0L

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = str(fob.read(valueSize))
        self.value = value
        
class PFSTagString(PFSBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 2
        self.value = ""

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = str(fob.read(valueSize))
        self.value = value
        
class PFSTagList(PFSBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 5
        self.value = []
    
    def write(self, fob):
        nameLength = str(len(str(self.tagName)))
        valueLength = str(len(self.value))
        text = "%d%s:%s:%s" % (self.type, nameLength, valueLength, self.tagName)
        fob.write(text)
        
        for tag in self.value:
            tag.write(fob)

    def read(self, fob, compoundNameSize, compoundValueSize):
        self.tagName = fob.read(compoundNameSize)
        for i in range(compoundValueSize):
            id = int(fob.read(1))
            charFound = 0;
            nameSize = ""
            valueSize = ""
            
            while charFound < 2:
                lastChar = fob.read(1)
                if(lastChar == ":"):
                    charFound = charFound + 1
                elif(charFound == 0):
                    nameSize += nameSize + lastChar
                elif(charFound == 1):
                    valueSize = valueSize + lastChar
                   
            nameSize = int(nameSize)
            valueSize = int(valueSize)  
             
            type = PFSBase.getTypeFromId(id)
            type.read(fob, nameSize, valueSize)
            self.value.append(type)
    
    def tagCount(self):
        return len(self.value)
    
    def appendTag(self, tag):
        self.value.append(tag)
        return self
    
    def removeTag(self, tagName):
        pos = self.getPositionOfTag(tagName)
        if pos != -1:
            self.value[pos:pos+1] = []
        return self
    
    def printValues(self, indent):
        realIndent = ""
        for i in range(indent):
            realIndent += "   "
        print realIndent + "TAG_LIST", ":", self.tagName
        
        indent += 1
        for i in self.value:
            i.printValues(indent)

    def getPositionOfTag(self, tagName):
        count = 0
        for tag in self.value:
            if tag.tagName == tagName:
                return count
            count = count + 1
        return -1

class PFSTagCompound(PFSBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 6
        self.value = []

    def write(self, fob):
        nameLength = str(len(str(self.tagName)))
        valueLength = str(len(self.value))
        text = "%d%s:%s:%s" % (self.type, nameLength, valueLength, self.tagName)
        fob.write(text)
        
        for tag in self.value:
            tag.write(fob)

    def read(self, fob, compoundNameSize, compoundValueSize):
        self.tagName = fob.read(compoundNameSize)
        for i in range(compoundValueSize):
            id = int(fob.read(1))
            charFound = 0;
            nameSize = ""
            valueSize = ""
            
            while charFound < 2:
                lastChar = fob.read(1)
                if(lastChar == ":"):
                    charFound = charFound + 1
                elif(charFound == 0):
                    nameSize += nameSize + lastChar
                elif(charFound == 1):
                    valueSize = valueSize + lastChar
                   
            nameSize = int(nameSize)
            valueSize = int(valueSize)  
             
            type = PFSBase.getTypeFromId(id)
            type.read(fob, nameSize, valueSize)
            self.value.append(type)

    
    def printValues(self, indent):
        realIndent = ""
        for i in range(indent):
            realIndent += "   "
        print realIndent + "TAG_COMPOUND", ":", self.tagName
        
        indent += 1
        for i in self.value:
            i.printValues(indent)

    
    def addTag(self, tag):
        if self.hasTag(tag.tagName):
            pos = self.getPositionOfTag(tag.tagName)
            self.value[pos] = tag
        else:
            self.value.append(tag)
        return self

    def setInteger(self, tagName, value):
        self.addTag(PFSTagInt(tagName).setValue(value))
        return self
    
    def setString(self, tagName, value):
        self.addTag(PFSTagString(tagName).setValue(value))
        return self
    
    '''
    @param tagName: The tag name that will be used for later lookup
    @param value: The integer value to be saved 
    @return: The object pointer.
    '''
    def setFloat(self, tagName, value):
        self.addTag(PFSTagFloat(tagName).setValue(value))
        return self
    
    def setLong(self, tagName, value):
        self.addTag(PFSTagLong(tagName).setValue(value))
        return self

    '''
    Searches through the array and looks for a tag with name 'tagName'
    @param tagName: The tag name used for the lookup
    @return: The tag associated with the given string
    '''
    def getTag(self, tagName):
        for tag in self.value:
            if tag.tagName == tagName:
                return tag
        return 0 

    def hasTag(self, tagName):
        for tag in self.value:
            if tag.tagName == tagName:
                return True
        return False

    def getPositionOfTag(self, tagName):
        count = 0
        for tag in self.value:
            if tag.tagName == tagName:
                return count
            count = count + 1
        return -1
        