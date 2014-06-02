import socket
import sys
import struct
from datacomplier import dataoutput, datainput
from packet import packet, register_channel, write_packet, recive_packet
from _thread import *
 
HOST = socket.gethostname()   # Symbolic name meaning all available interfaces
PORT = 12345                  # Arbitrary non-privileged port
CLIENTS = {}

p = 258
p = p >> 8
print(p)
p = p << 8
print(p)

t = struct.pack('>I', -1213121232)
for i in t:
    print(i)
print(struct.unpack('>I', t))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))

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

print('Socket bind complete')

#Start listening on socket
s.listen(10)
print('Socket now listening')


#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send(write_packet(packetconnect().set_message('dwaeadwfaerwe'), packetconnect().set_message('TWICE'))) #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        try:
            #Receiving from client
            data = conn.recv(1024)
            test = dataoutput()
            test.writeString('test')
            test.write(2)
            test.writeString('test working')
            
            reply = 'OK...' + str(data, 'UTF-8')

            #Send all other clients the message
            for i in CLIENTS.keys():
                if i is not s and i is not conn: #i is not this server socket and i is not the socket the message was recived from
                    i.send(test.data)
            
            #conn.sendall(bytes(reply, 'UTF-8'))
        except ConnectionResetError:
            break

    #Connection with client was lost
    print('Connection with %s:%s was lost' % (CLIENTS[conn][0], CLIENTS[conn][1]))
    CLIENTS.pop(conn)
    conn.close()

#now keep talking with the client
while True:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    CLIENTS[conn] = (addr[0], addr[1])
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
