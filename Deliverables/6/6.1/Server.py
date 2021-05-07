import socket
import json

d = json.JSONDecoder()
e = json.JSONEncoder()

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12343                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print(host)

s.listen(5)                 # Now wait for client connection.
board = {"black":["bar",2,2,2,2,4,5,6,7,13,13,13,13,24,24],"white":["bar","bar",12,12,12,12,12,17,17,17,19,19,19,19,19]}
dict = {'take-turn' : [board, [2,2,2,2]]}
string = e.encode(dict)

while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   c.send(bytes(string, 'utf-8'))
   decodedstr = d.decode(c.recv(1024).decode())
   print(decodedstr)
   c.close()                # Close the connection