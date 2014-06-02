import socket               # Import socket module

clients = []

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   clients.append(c)
   for client in clients:
      c.send(bytes('test', 'UTF-8'))
   print('Got connection from', addr)
   c.send(bytes('Thank you for connecting', 'UTF-8'))

for client in clients:
   c.close()

while True:
    pass
