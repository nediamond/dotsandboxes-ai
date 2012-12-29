import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
import copy
class ClientChannel(PodSixNet.Channel.Channel):
	def __init__(self, *args, **kwargs):
		PodSixNet.Channel.Channel.__init__(self, *args, **kwargs)
		self.turn = 0
		# Seven lines in each direction to make a six by six grid.
		self.boardh = [[False for x in range(6)] for y in range(7)]
		self.boardv = [[False for x in range(7)] for y in range(6)]
	def Network_place(self, data):
		hv = data["hv"]
		x = data["x"]
		y = data["y"]
		if hv=="h":
			self.boardh[y][x] = True
		else:
			self.boardv[y][x] = True
		if self.turn==0:
			self.turn=1
			self._server.player1.Send(data)
		elif self.turn==1:
			self.turn=0
			self._server.player0.Send(data)
		print self.turn

class BoxesServer(PodSixNet.Server.Server):
	channelClass = ClientChannel
	def __init__(self, *args, **kwargs):
		PodSixNet.Server.Server.__init__(self, *args, **kwargs)
		self.player0=None
		self.player1=None
	def Connected(self, channel, addr):
		if self.player0==None:
			self.player0=channel
		elif self.player1==None:
			self.player1=channel
			self.player0.Send({"action": "receivedata","player":0})
			self.player1.Send({"action": "receivedata","player":1})
boxesServe = BoxesServer()
print "STARTING SERVER ON LOCALHOST:3456"
while True:
	boxesServe.Pump()
	sleep(0.01)