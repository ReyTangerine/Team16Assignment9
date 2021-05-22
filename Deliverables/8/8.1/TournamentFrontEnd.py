import socket
import json
import sys
from copy import deepcopy
from Administrator_Class import Admin
from Tournament_Class import Tournament

d = json.JSONDecoder()
e = json.JSONEncoder()
s = socket.socket()  # Create a socket object

### On STDIN we're receiving
### config ::= { "players" : number, "port" : number, "type" : type }
### type ::= "round robin" | "single elimination"

## admin-config::= { "local" : local-strategy, "port" : number }
config = sys.stdin.read()
config = d.decode(config)
port = config["port"]  # Reserve a port for your service.

noPlayers = config["players"]
tourneyType = config["type"]

s.bind(("", port))  # Bind to the port
ourTourney = Tournament(tourneyType, noPlayers, s)
ourTourney.matching()
ourTourney.tournamentResult()
