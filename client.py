
from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
	def __init__(self, address):
		try:
			if not address:
				host, port="localhost", 8000
			else:
				host,port=address.split(":")
			self.Connect((host, int(port)))
		except:
			print "Error Connecting to Server"
			print "Usage:", "host:port"
			print "e.g.", "localhost:31425"
			exit()
		print "Boxes client started"
		self.input1 = []
	def Loop(self):
		connection.Pump()
		self.Pump()
	# built in stuff
	def Network(self, data):
		self.input1.append(data)
	def Network_connected(self, data):
		print "You are now connected to the server"
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()