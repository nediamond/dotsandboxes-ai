
from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
	def __init__(self, ):
		self.Connect()
		print "Boxes client started"
		self.input1 = 0
	def Loop(self):
		connection.Pump()
		self.Pump()
	# built in stuff
	def Network(self, data):
		print data
		if data["action"]!="yourturn":
			self.input1 = data
	def Network_yourturn(self, data):
		if data["data"]==True:
			print data["data"]
			self.input1=data
	def Network_connected(self, data):
		print "You are now connected to the server"
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()