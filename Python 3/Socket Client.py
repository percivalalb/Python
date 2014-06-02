import socket               # Import socket module
from datacomplier import dataoutput, datainput
from packet import packet, register_channel, write_packet, recive_packet
from _thread import *

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))

class packetconnect(packet):

    def __init__(self):
        packet.__init__(self, 'connect')

    def set_message(self, message):
        self.message = message
        return self
        
    def write(self, do):
        do.writeString(self.message)
    
    def read(self, di):
        self.message = di.readString()

    def execute(self):
        print(self.message)

register_channel('connect', packetconnect)

def recievethread():
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        try:
            recive_packet(s.recv(1024))
            
        except ConnectionResetError:
            break
    


start_new_thread(recievethread ,())

while True:
    s.send(bytes(input(), 'UTF-8'))
s.close                     # Close the socket when done

while True:
    pass
