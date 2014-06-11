import socket
import sys
from _thread import *
import subprocess

host = socket.gethostname()   # Symbolic name meaning all available interfaces
port = 2                  # Arbitrary non-privileged port
CLIENTS = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("-" * 60)
print('Socket created on %s port %d' % (host, port))

s.bind((host, port))

print('Socket bind complete')

#Start listening on socket
s.listen(10)
print('Socket now listening')
print("-" * 60)

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send(bytes('Welcome to the Server', 'UTF-8')) #send only takes string
    
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        try:
            #Receiving from client
            data = conn.recv(1024)
            
            reply = str(data, 'UTF-8')
            print(reply)
            #Send all other clients the message
            for i in CLIENTS.keys():
                if i is not s: #and i is not conn: #i is not this server socket and i is not the socket the message was recived from
                    i.sendall(bytes(reply, 'UTF-8'))
            
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
