


class dataoutput():

    def __init__(self):
        self.data = bytearray()

    def writeByte(self, byte):
        assert(byte >= 0 and byte <= 255), 'Can\'t write a %d as a byte' % byte
        self.data.append(byte)

    def writeInteger(self, integer):
        negative = integer < 0
        
        integer = integer << 1 #Move the binary version 1 to the left, e.g 1101 (13) becomes 11010 (26)
        
        if negative: integer = -integer; integer = integer | 1; #If integer is negative the free bit in number is converted to a 1 and integer
        no_bytes = 0
        while integer >= 2**(no_bytes * 8): no_bytes += 1 #Figures out how many bytes the integer takes up

        self.writeByte(no_bytes) #Writes the number of bytes for when it is read
        for byte in range(no_bytes):
            mask = 2**(8 * byte + 8) - 2**(byte * 8) #Creates a mask to remove all bits but that of the byte to be written
            
            final = (integer & mask) >> (byte * 8) #Applies the mask and shifts the target byte to the front making a number between 0-255
            self.writeByte(final)

    def writeIntegerArray(self, array):
        self.writeInteger(len(array))
        for integer in array:
            self.writeInteger(int(integer))

    def writeFloat(self, _float):
        self.writeString(str(_float))

    def writeFloatArray(self, array):
        self.writeInteger(len(array))
        for _float in array:
            self.writeFloat(_float)
    
    def writeString(self, string):
        self.writeInteger(len(string))
        for char in string:
            self.writeInteger(ord(char))

    def writeStringArray(self, array):
        self.writeInteger(len(array))
        for string in array:
            self.writeString(string)
    
    def writeBoolean(self, boolean):
        self.writeByte(int(boolean)) #Converts boolean to one bit True (1), False (0)

    def writeBooleanArray(self, array):
        integer = 0
        length = len(array)
        
        for count in range(length):
            if array[count]:
                integer = integer | 2**(length - count - 1)
                
        integer = integer | 2**(length) #Adds a marker to show you where the array starts because [False] in an array would be undetectable
        self.writeInteger(integer)
    
class datainput():

    def __init__(self, data, index = 0):
        self.index = index
        self.data = data

    def readByte(self):
        byte = self.data[self.index]
        self.index += 1
        return byte

    def readInteger(self):
        no_bytes = self.readByte()
        integer = 0
        for byte in range(no_bytes):
            integer += self.readByte() << (byte * 8)
        negative = integer % 2 == 1
        integer = integer >> 1
        if negative: integer = -integer
        return integer

    def readIntegerArray(self):
        array = []
        length = self.readInteger()
        for i in range(length):
            array.append(self.readInteger())
        return array

    def readFloat(self):
        return float(self.readString())

    def readFloatArray(self):
        array = []
        length = self.readInteger()
        for i in range(length):
            array.append(self.readFloat())
        return array
        
    def readString(self):
        string = ''
        length = self.readInteger()
        for i in range(length):
            string += chr(self.readInteger())
        return string

    def readStringArray(self):
        array = []
        length = self.readInteger()
        for i in range(length):
            array.append(self.readString())
        return array

    def readBoolean(self):
        return self.readByte() == 1

    def readBooleanArray(self):
        carrier_integer = self.readInteger()
        binary = bin(carrier_integer)
        length = len(binary) - 3
        array = []
        for i in range(2, 2 + length):
            array.append(int(binary[i + 1]) == 1)
        
        return array

    def has_read_everything(self):
        return len(self.data) <= self.index

do = dataoutput()
do.writeInteger(-2)
print('Size of data %d' % len(do.data))
di = datainput(do.data)
print(di.readInteger())
