from savehandler import tagcompound

class dataoutput():

    def __init__(self):
        self.data = bytearray()

    def write_byte(self, byte):
        assert(byte >= 0 and byte <= 255), 'Can\'t write a %d as a byte' % byte
        self.data.append(byte)

    def write_integer(self, integer):
        negative = integer < 0
        
        integer = integer << 1 #Move the binary version 1 to the left, e.g 1101 (13) becomes 11010 (26)
        
        if negative: integer = -integer; integer = integer | 1; #If integer is negative the free bit in number is converted to a 1 and integer
        no_bytes = 0
        while integer >= 2**(no_bytes * 8): no_bytes += 1 #Figures out how many bytes the integer takes up

        self.write_byte(no_bytes) #Writes the number of bytes for when it is read
        for byte in range(no_bytes):
            mask = 2**(8 * byte + 8) - 2**(byte * 8) #Creates a mask to remove all bits but that of the byte to be written
            
            final = (integer & mask) >> (byte * 8) #Applies the mask and shifts the target byte to the front making a number between 0-255
            self.write_byte(final)

    def write_integer_array(self, array):
        self.write_integer(len(array))
        for integer in array:
            self.write_integer(int(integer))

    def write_float(self, _float):
        self.write_string(str(_float))

    def write_float_array(self, array):
        self.write_integer(len(array))
        for _float in array:
            self.write_float(_float)
    
    def write_string(self, string):
        self.write_integer(len(string))
        for char in string:
            self.write_integer(ord(char))

    def write_string_array(self, array):
        self.write_integer(len(array))
        for string in array:
            self.write_string(string)
    
    def write_boolean(self, boolean):
        self.write_byte(int(boolean)) #Converts boolean to one bit True (1), False (0)

    def write_boolean_array(self, array):
        integer = 0
        length = len(array)
        
        for count in range(length):
            if array[count]:
                integer = integer | 2**(length - count - 1)
                
        integer = integer | 2**(length) #Adds a marker to show you where the array starts because [False] in an array would be undetectable
        self.write_integer(integer)

    def write_tag_compound(self, compound):
        pass
    
class datainput():

    def __init__(self, data, index = 0):
        self.index = index
        self.data = data

    def read_byte(self):
        byte = self.data[self.index]
        self.index += 1
        return byte

    def read_integer(self):
        no_bytes = self.read_byte()
        integer = 0
        for byte in range(no_bytes):
            integer += self.read_byte() << (byte * 8)
        negative = integer % 2 == 1
        integer = integer >> 1
        if negative: integer = -integer
        return integer

    def read_integer_array(self):
        array = []
        length = self.read_integer()
        for i in range(length):
            array.append(self.read_integer())
        return array

    def read_float(self):
        return float(self.read_string())

    def read_float_array(self):
        array = []
        length = self.read_integer()
        for i in range(length):
            array.append(self.read_float())
        return array
        
    def read_string(self):
        string = ''
        length = self.read_integer()
        for i in range(length):
            string += chr(self.read_integer())
        return string

    def read_string_array(self):
        array = []
        length = self.read_integer()
        for i in range(length):
            array.append(self.read_string())
        return array

    def read_boolean(self):
        return self.readByte() == 1

    def read_boolean_array(self):
        carrier_integer = self.read_integer()
        binary = bin(carrier_integer)
        length = len(binary) - 3
        array = []
        for i in range(2, 2 + length):
            array.append(int(binary[i + 1]) == 1)
        
        return array

    def read_tag_compound(self):
        pass
    
    def has_read_everything(self):
        return len(self.data) <= self.index

do = dataoutput()
do.write_integer(-2)
print('Size of data %d' % len(do.data))
di = datainput(do.data)
print(di.read_integer())
