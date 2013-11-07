import os

class NBTBase:
    
    MAPPING = ['NULL', 'INT', 'STRING', 'FLOAT', 'LONG', 'COMPOUND']
    DIGITS = 3
    
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 0
        self.value = NULL

    def write(self, fob):
        return

    def read(self, fob, nameSize, valueSize):
        return
    
    def setValue(self, value):
        self.value = value
        return self

    @staticmethod
    def getTypeFromId(id):
        if id == 0:
            return null
        elif id == 1:
            return NBTTagInt("")
        elif id == 2:
            return NBTTagString("")
        elif id == 3:
            return NBTTagFloat("")
        elif id == 4:
            return NBTTagLong("")
        elif id == 5:
            return NBTTagCompound("")
        return NULL

    @staticmethod
    def readFromFile(fileLoc):
        'Creates a new file if none exits'
        open(fileLoc, 'a').close()
        fob = open(fileLoc, 'r+')
        fileSize = int(os.path.getsize(fileLoc))
        data = []
        while fileSize > fob.tell():
            id = int(fob.read(1))
            nameSize = int(fob.read(NBTBase.DIGITS))
            valueSize = int(fob.read(NBTBase.DIGITS))
            type = NBTBase.getTypeFromId(id)
            type.read(fob, nameSize, valueSize)
            data.append(type)
            
        fob.close()
        tagCompound = NBTTagCompound("")
        tagCompound.value = data
        return tagCompound

    @staticmethod
    def writeToFile(fileLoc, tagCompound):
        fob = open(fileLoc, 'w+')
        for tag in tagCompound.value:
            tag.write(fob)
        fob.close()
        

class NBTTagInt(NBTBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 1
        self.value = 0

    def write(self, fob):
        nameLength = str(len(str(self.tagName)))
        while len(nameLength) < NBTBase.DIGITS:
            nameLength = "0" + nameLength
        valueLength = str(len(str(self.value)))
        while len(valueLength) < NBTBase.DIGITS:
            valueLength = "0" + valueLength
        fob.write(str(self.type) + nameLength + valueLength + self.tagName + str(self.value))

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = int(fob.read(valueSize))
        self.value = value

class NBTTagString(NBTBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 2
        self.value = ""

    def write(self, fob):
        nameLength = str(len(str(self.tagName)))
        while len(nameLength) < NBTBase.DIGITS:
            nameLength = "0" + nameLength
        valueLength = str(len(str(self.value)))
        while len(valueLength) < NBTBase.DIGITS:
            valueLength = "0" + valueLength
        fob.write(str(self.type) + nameLength + valueLength + self.tagName + str(self.value))

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = str(fob.read(valueSize))
        self.value = value

class NBTTagFloat(NBTBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 3
        self.value = 0.0

    def write(self, fob):
        nameLength = str(len(str(self.tagName)))
        while len(nameLength) < NBTBase.DIGITS:
            nameLength = "0" + nameLength
        valueLength = str(len(str(self.value)))
        while len(valueLength) < NBTBase.DIGITS:
            valueLength = "0" + valueLength
        fob.write(str(self.type) + nameLength + valueLength + self.tagName + str(self.value))

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = float(fob.read(valueSize))
        self.value = value

class NBTTagString(NBTBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 4
        self.value = 0L

    def write(self, fob):
        nameLength = str(len(str(self.tagName)))
        while len(nameLength) < NBTBase.DIGITS:
            nameLength = "0" + nameLength
        valueLength = str(len(str(self.value)))
        while len(valueLength) < NBTBase.DIGITS:
            valueLength = "0" + valueLength
        fob.write(str(self.type) + nameLength + valueLength + self.tagName + str(self.value))

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = str(fob.read(valueSize))
        self.value = value

class NBTTagCompound(NBTBase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 5
        self.value = []

    def write(self, fob):
        nameLength = str(len(str(self.tagName)))
        while len(nameLength) < NBTBase.DIGITS:
            nameLength = "0" + nameLength
        valueLength = str(len(str(self.value)))
        while len(valueLength) < NBTBase.DIGITS:
            valueLength = "0" + valueLength
        fob.write(str(self.type) + nameLength + valueLength + self.tagName + str(self.value))

    def read(self, fob, size):
        for i in range(size):
            id = int(fob.read(1))
            nameSize = int(fob.read(NBTBase.DIGITS))
            valueSize = int(fob.read(NBTBase.DIGITS))
            type = NBTBase.getTypeFromId(id)
            type.read(fob, nameSize, valueSize)
            value.append(type)

    def addTag(self, tag):
        self.value.append(tag)

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
    
