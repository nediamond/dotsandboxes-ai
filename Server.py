# just some imports
import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

#client channel
#INITIALIZED EVERY TIME CLIENT CONNECTS!
class ClientChannel(PodSixNet.Channel.Channel):
	def __init__(self, *args, **kwargs):
		PodSixNet.Channel.Channel.__init__(self, *args, **kwargs)

		#id of the game the client is in
		self.gameid=0
	#Network activity with action of place
	def Network_place(self, data):
		#deconsolidate all of the data from the dictionary

		#horizontal or vertical?
		hv = data["hv"]

		#x of placed line
		x = data["x"]

		#y of placed line
		y = data["y"]

		#player number (1 or 0)
		num=data["player"]

		#id of game given by server at start of game
		self.gameid = data["gameid"]

		#tells server to place line
		self._server.placeLine(hv=="h", x, y, data, self.gameid, num)
	#tell server to close game	
	def Close(self):
		self._server.close(self.gameid)

#custom class for a game
class Game:
	def __init__(self, player0, currentIndex):
		# whose turn (1 or 0)
		self.turn = 0
		#owner map
		self.owner=[[False for x in range(6)] for y in range(6)]
		# Seven lines in each direction to make a six by six grid.
		self.boardh = [[False for x in range(6)] for y in range(7)]
		self.boardv = [[False for x in range(7)] for y in range(6)]

		#initialize the players including the one who started the game
		self.player0=player0
		self.player1=None

		#gameid of game
		self.gameid=currentIndex
	#placeLine
	def placeLine(self, is_h, x, y, data, num):
		#make sure it's their turn
		if num==self.turn:
			#place line in game
			if is_h:
				self.boardh[y][x] = True
			else:
				self.boardv[y][x] = True
			#send data and turn data to each player
			self.player0.Send(data)
			self.player1.Send(data)
			self.player1.Send({"action":"yourturn", "torf":True if self.turn==1 else False})
			self.player0.Send({"action":"yourturn", "torf":True if self.turn==0 else False})
			#switch turns
			self.turn=0 if self.turn==1 else 1
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
			for time in range(2):
				for y in range(6):
					for x in range(6):
						if game.boardh[y][x] and game.boardv[y][x] and game.boardh[y+1][x] and game.boardv[y][x+1] and not game.owner[x][y]:
							if self.games[index].turn==0:
								self.games[index].owner[x][y]=2
								game.player1.Send({"action":"win", "x":x, "y":y})
								game.player0.Send({"action":"lose", "x":x, "y":y})
								change=1
							else:
								self.games[index].owner[x][y]=1
								game.player0.Send({"action":"win", "x":x, "y":y})
								game.player1.Send({"action":"lose", "x":x, "y":y})
								change=0
			self.games[index].turn = change if change!=3 else self.games[index].turn
			print self.games[index].turn
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
	def placeLine(self, is_h, x, y, data, gameid, num):
		game = [a for a in self.games if a.gameid==gameid]
		if len(game)==1:
			game[0].placeLine(is_h, x, y, data, num)
# try:
address=raw_input("Host:Port (localhost:8000): ")
if not address:
	host, port="localhost", 8000
else:
	host,port=address.split(":")
boxesServe = BoxesServer(localaddr=(host, int(port)))
# except:
# 	print "Usage:", "host:port"
# 	print "e.g.", "localhost:31425"
# 	exit()
print "STARTING SERVER ON LOCALHOST:3456"
while True:
	boxesServe.loop()
	sleep(0.01)