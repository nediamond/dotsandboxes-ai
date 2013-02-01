import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
import copy
class ClientChannel(PodSixNet.Channel.Channel):
	def __init__(self, *args, **kwargs):
		PodSixNet.Channel.Channel.__init__(self, *args, **kwargs)
		self.gameid=0
	def Network_place(self, data):
		hv = data["hv"]
		x = data["x"]
		y = data["y"]
		num=data["player"]
		self.gameid = data["gameid"]
		self._server.performGameAction(hv=="h", x, y, data, self.gameid, num)
	def Close(self):
		self._server.close(self.gameid)

class Game:
	def __init__(self, player0, currentIndex):
		self.turn = 0
		self.winning=[[False for x in range(6)] for y in range(6)]
		# Seven lines in each direction to make a six by six grid.
		self.boardh = [[False for x in range(6)] for y in range(7)]
		self.boardv = [[False for x in range(7)] for y in range(6)]
		self.player0=player0
		self.player1=None
		self.gameid=currentIndex
	def performGameAction(self, is_h, x, y, data, num):
		print "Start:", self.turn, num
		if num==self.turn:
			if is_h:
				self.boardh[y][x] = True
			else:
				self.boardv[y][x] = True
			if self.turn==0:
				self.turn=1
				self.player1.Send(data)
				self.player0.Send(data)
				self.player1.Send({"action":"yourturn", "torf":True if self.turn==1 else False})
				self.player0.Send({"action":"yourturn", "torf":True if self.turn==0 else False})
			elif self.turn==1:
				self.turn=0
				self.player0.Send(data)
				self.player1.Send(data)
				self.player1.Send({"action":"yourturn", "torf":True if self.turn==1 else False})
				self.player0.Send({"action":"yourturn", "torf":True if self.turn==0 else False})
		print "End:", self.turn
class BoxesServer(PodSixNet.Server.Server):
	channelClass = ClientChannel
	def __init__(self, *args, **kwargs):
		PodSixNet.Server.Server.__init__(self, *args, **kwargs)
		self.games = []
		self.queue = None
		self.currentIndex=0
	def close(self, gameid):
		game = [a for a in self.games if a.gameid==gameid][0]
		game.player0.Send({"action":"close"})
		game.player1.Send({"action":"close"})
	def loop(self):
		# Check for any wins
		# Loop through all of the squares
		index=0
		change=3
		for game in self.games:
			change=3
			for y in range(6):
				for x in range(6):
					if game.boardh[y][x] and game.boardv[y][x] and game.boardh[y+1][x] and game.boardv[y][x+1] and not game.winning[x][y]:
						if self.games[index].turn==0:
							self.games[index].winning[x][y]=2
							game.player1.Send({"action":"win", "x":x, "y":y})
							game.player0.Send({"action":"lose", "x":x, "y":y})
							change=1
						else:
							self.games[index].winning[x][y]=1
							game.player0.Send({"action":"win", "x":x, "y":y})
							game.player1.Send({"action":"lose", "x":x, "y":y})
							change=0
			self.games[index].turn = change if change!=3 else self.games[index].turn
			game.player1.Send({"action":"yourturn", "torf":True if self.games[index].turn==1 else False})
			game.player0.Send({"action":"yourturn", "torf":True if self.games[index].turn==0 else False})
			index+=1
		self.Pump()
	def Connected(self, channel, addr):
		if self.queue==None:
			self.queue=Game(channel, self.currentIndex)
			channel.gameid=self.currentIndex
			self.currentIndex+=1
		else:
			self.queue.player1=channel
			self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
			self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
			self.games.append(self.queue)
			self.queue=None
	def performGameAction(self, is_h, x, y, data, gameid, num):
		game = [a for a in self.games if a.gameid==gameid][0]
		game.performGameAction(is_h, x, y, data, num)
try:
	address=raw_input("Host:Port (localhost:8000): ")
	if not address:
		host, port="localhost", 8000
	else:
		host,port=address.split(":")
	boxesServe = BoxesServer(localaddr=(host, int(port)))
except:
	print "Usage:", "host:port"
	print "e.g.", "localhost:31425"
	exit()
print "STARTING SERVER ON LOCALHOST:3456"
while True:
	boxesServe.loop()
	sleep(0.01)