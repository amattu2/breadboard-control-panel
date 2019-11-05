'''
	Produced 2019
	By https://github.com/amattu2
	Copy Alec M.
	License GNU Affero General Public License v3.0
'''

'''
	Status Codes:
		0001: New Client
		0002:
		0003: New Color
'''

'''
	Todo:
	- Beep x2 for user connects
	- Beep x1 for user disconnect
	- Handle LEDs
	- Implement "activeColor" and broadcast that with all events
'''

# Imports
import json
from assets.wsserver import WebsocketServer, OPCODE_CLOSE_CONN
from datetime import datetime

# Variables
server = WebsocketServer(8443)
logs = []
colors = {"red": 1, "green": 2, "blue": 3}

# Handlers
def connect(client, server):
	# Checks
	if (not server): return False
	if (not client): return False

	# Notice
	print('[NOTICE] Client Connected: #{0}'.format(client['id']))
	broadcast(server, {"status": "0001", "client": client['id'], "clients": getClients(server), "logs": logs})

def disconnect(client, server):
	# Checks
	if (not server): return False
	if (not client): return False

	# Notice
	print('[NOTICE] Client Disconnected: #{0}'.format(client['id']))

def disconnectClient(client):
	# Checks
	if (not 'handler' in client): return False

	# Close
	client['handler'].send_text("", opcode = OPCODE_CLOSE_CONN)

def getClients(server):
	# Checks
	if (not server): return False

	# Variables
	clients = []

	# Loops
	for client in server.get_clients():
		clients.append({"address": "{0}:{1}".format(client["address"][0], client["address"][1]), "timestamp": client["timestamp"]})

	# Return
	return clients

def log(color, client):
	logs.append({"color": color, "client": "{0}:{1}".format(client["address"][0], client["address"][1]), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

def broadcast(server, message = {}):
	# Checks
	if (not server): return False

	# Variables
	data = json.dumps(message, separators=(',', ':'))

	# Broadcast
	server.send_message_to_all(data)

def navigator(client, server, message):
	# Attempts
	try:
		message = json.loads(message)
	except:
		return False

	# Checks
	if (not server): return False
	if (not client): return False
	if (not 'address' in client): return False
	if (not type(message) is dict):
		# Force Disconnect
		disconnectClient(client)
		return False
	if (not 'function' in message):
		# Force Disconnect
		disconnectClient(client)
		return False

	# Navigator
	if (message['function'] == 'changeColor'):
		# Variables
		result = changeColor(message, client)

		# Checks
		if (result == True):
			broadcast(server, {"status": "0003", "client": client['id'], "color": message["color"], "logs": logs})
	else:
		return False

# Change Color
def changeColor(message, client):
	# Checks
	if (not message): return False
	if (not client): return False
	if (not 'color' in message or not message['color'] in colors): return False

	# Success
	log(message['color'], client)
	print("New Color: {0} [#{1}]".format(message['color'], colors[message['color']]))
	return True

# Properties
server.set_fn_new_client(connect)
server.set_fn_client_left(disconnect)
server.set_fn_message_received(navigator)
server.run_forever()
