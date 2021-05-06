import socket
import json

d = json.JSONDecoder()
e = json.JSONEncoder()

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print(host)

s.listen(5)                 # Now wait for client connection.

string = b"This is a byte object i hope"

while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   c.send(string)
   c.close()                # Close the connection