import os

def get_type_from_id(id):
    if id == 0:
        return 0
    elif id == 1:
        return tagint("")
    elif id == 2:
        return tagstring("")
    elif id == 3:
        return tagfloat("")
    elif id == 5:
        return taglist("")
    elif id == 6:
        return tagcompound("")
    return 0

def readFromFile(file_location):
    'Creates a new file if none exits'
    open(file_location, 'a').close()
    fob = open(file_location, 'r+')
    fileSize = int(os.path.getsize(file_location))
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
        type = get_type_from_id(id)
        type.read(fob, nameSize, valueSize)
        data.append(type)
            
    fob.close()
    tag_compound = tagcompound("")
    tag_compound.value = data
    return tag_compound

def writeToFile(file_location, tag_compound):
    fob = open(file_location, 'w+')
    for tag in tag_compound.value:
        tag.write(fob)
    fob.close()


class tagbase:
    
    MAPPING = ['NULL', 'INT', 'STRING', 'FLOAT', 'LONG', 'LIST', 'TAG_COMPOUND']
    
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
    
    def print_values(self, indent):
        realIndent = ""
        for i in range(indent):
            realIndent += "   "
        
        print(realIndent + tagbase.MAPPING[self.type], self.tagName, ":", self.value)
        return
    
    def setValue(self, value):
        self.value = value
        return self
        
class tagfloat(tagbase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 3
        self.value = 0.0

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = float(fob.read(valueSize))
        self.value = value
        
class tagint(tagbase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 1
        self.value = 0

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = int(fob.read(valueSize))
        self.value = value
        
class tagstring(tagbase):
    def __init__(self, tagName):
        self.tagName = tagName
        self.type = 2
        self.value = ""

    def read(self, fob, nameSize, valueSize):
        name = str(fob.read(nameSize))
        self.tagName = name
        value = str(fob.read(valueSize))
        self.value = value
        
class taglist(tagbase):
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
             
            type = get_type_from_id(id)
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
    
    def print_values(self, indent):
        realIndent = ""
        for i in range(indent):
            realIndent += "   "
        print(realIndent + "TAG_LIST", ":", self.tagName)
        
        indent += 1
        for i in self.value:
            i.print_values(indent)

    def getPositionOfTag(self, tagName):
        count = 0
        for tag in self.value:
            if tag.tagName == tagName:
                return count
            count = count + 1
        return -1

class tagcompound(tagbase):
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
             
            type = get_type_from_id(id)
            type.read(fob, nameSize, valueSize)
            self.value.append(type)

    
    def print_values(self, indent):
        realIndent = ""
        for i in range(indent):
            realIndent += "   "
        print(realIndent + "TAG_COMPOUND", ":", self.tagName)
        
        indent += 1
        for i in self.value:
            i.print_values(indent)

    
    def addTag(self, tag):
        if self.hasTag(tag.tagName):
            pos = self.getPositionOfTag(tag.tagName)
            self.value[pos] = tag
        else:
            self.value.append(tag)
        return self

    def setInteger(self, tagName, value):
        self.addTag(tagint(tagName).setValue(value))
        return self
    
    def setString(self, tagName, value):
        self.addTag(tagstring(tagName).setValue(value))
        return self
    
    '''
    @param tagName: The tag name that will be used for later lookup
    @param value: The integer value to be saved 
    @return: The object pointer.
    '''
    def setFloat(self, tagName, value):
        self.addTag(tagfloat(tagName).setValue(value))
        return self
    
    def setLong(self, tagName, value):
        self.addTag(taglong(tagName).setValue(value))
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

    def removeTag(self, tagName, tagType = -1):
        count = 0
        for tag in self.value:
            if tag.tagName == tagName and (tagType == -1 or tagType == tag.type):
                self.value.remove(tag)
            count = count + 1
        
