import pygame
class Enemy1:
	def __init__(self):
		self.humanname="Enemy #1"
		self.image=pygame.image.load("enemy1")
		self.health=10
		self.defense=5
		self.attack = 2
		self.reload = 2
	def defend(self, attacker):
		self.health-=attacker.attack-self.defense
	def attack(ship)