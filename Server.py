import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
import copy
class ClientChannel(PodSixNet.Channel.Channel):
	def __init__(self, *args, **kwargs):
		PodSixNet.Channel.Channel.__init__(self, *args, **kwargs)
	def Network_place(self, data):
		hv = data["hv"]
		x = data["x"]
		y = data["y"]
		if hv=="h":
			self._server.boardh[y][x] = True
		else:
			self._server.boardv[y][x] = True
		# Check for any wins
		# Loop through all of the squares
		if self._server.turn==0:
			self._server.turn=1
			self._server.player1.Send(data)
		elif self._server.turn==1:
			self._server.turn=0
			self._server.player0.Send(data)

class BoxesServer(PodSixNet.Server.Server):
	channelClass = ClientChannel
	def __init__(self, *args, **kwargs):
		PodSixNet.Server.Server.__init__(self, *args, **kwargs)
		self.turn = 0
		self.winning=[[False for x in range(6)] for y in range(6)]
		# Seven lines in each direction to make a six by six grid.
		self.boardh = [[False for x in range(6)] for y in range(7)]
		self.boardv = [[False for x in range(7)] for y in range(6)]
		self.player0=None
		self.player1=None
	def loop(self):
		for y in range(6):
			for x in range(6): 
				if self.boardh[y][x] and self.boardv[y][x] and self.boardh[y+1][x] and self.boardv[y][x+1] and not self.winning[x][y]:
					if self.turn==0:
						print "2"
						self.winning[x][y]=2
						self.player1.Send({"action":"win", "x":x, "y":y})
						self.player0.Send({"action":"lose", "x":x, "y":y})
					else:
						print "1"
						self.winning[x][y]=1
						self.player0.Send({"action":"win", "x":x, "y":y})
						self.player1.Send({"action":"lose", "x":x, "y":y})
		self.Pump()
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
	boxesServe.loop()
	sleep(0.01)