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

# Imports
import json
from assets.wsserver import WebsocketServer
from assets.wsserver import OPCODE_CLOSE_CONN

# Variables
server = WebsocketServer(8443)

# Handlers
def connect(client, server):
	# Checks
	if (not server): return False
	if (not client): return False

	# Notice
	print('[NOTICE] Client Connected: #{0}'.format(client['id']))
	broadcast(server, {"status": "0001", "client": client['id']})

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
		print("Change color")
		broadcast(server, {"status": "0003", "client": client['id'], "color": "TBD"})
	else:
		return False

# Properties
server.set_fn_new_client(connect)
server.set_fn_client_left(disconnect)
server.set_fn_message_received(navigator)
server.run_forever()
