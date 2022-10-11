import pygame
import os
from PIL import Image
from PIL import ImageOps
import tile
import caves
import random

def flip(image):
	return pygame.transform.flip(image, True, False)

def flop(image):
	return pygame.transform.flip(image, False, True)

def flipflop(image):
	return pygame.transform.flip(image, True, True)

class Level:
	def __init__(self, screen:pygame.Surface):
		self.cave = caves.cave()
		self.screen = screen
		self.position = [0, 0]
		self.layout = []
		self.tiles = []
		self.backwalls = []
		self.liquids = []
		self.framecounter = 0
		
		self.level1()
		
	def level1(self):
		file = open("LevelFile.txt")
		self.layout = file.readlines()

		for row in range(len(self.layout)):
			for col in range(len(self.layout[row])):
				cell = self.layout[row][col]
				if cell == "g":
					self.grass(row, col)
				elif cell == "w":
					self.liquid("water", row, col)
				elif cell == "s":
					self.deco("drain", row, col)
				elif cell == "f":
					self.deco("narrow fall", row , col)
					
	def grass(self, row, col):
		x = col * 40
		y = row * 40
		t = tile.Tile(x, y, 40, 40)
		t.image.set_colorkey([0, 0, 0])

		solid = ([self.cave[0][0]] * 8 + 
		[self.cave[2][1], pygame.transform.flip(self.cave[2][1], True, False)] +
		[self.cave[0][1], pygame.transform.flip(self.cave[0][1], True, False)] + 
		[self.cave[0][2], pygame.transform.flip(self.cave[0][2], True, False)])
		ground = self.cave[1][1]
		edge = self.cave[1][0]
		corner = self.cave[1][2]
		wall = self.cave[2][0]
		underedge = self.cave[3][0]
		ceiling = self.cave[3][1]

		#True if there is a block next to the current position in the corresponding direction
		up = True
		down = True
		left = True
		right = True

		if row > 0 and self.layout[row - 1][col] != "g":
			up = False
		if row < len(self.layout) - 1 and self.layout[row + 1][col] != "g":
			down = False
		if col > 0 and self.layout[row][col - 1] != "g":
			left = False
		if col < len(self.layout[row]) - 1 and self.layout[row][col + 1] != "g":
			right = False


		t.image.blit(random.choice(solid), [0, 0])
		if not left:
			t.image.blit(wall, [0, 0])
		if not right:
			t.image.blit(flip(wall), [0, 0])
		if not up:
			t.image.blit(ground, [0, 0])
			if not left:
				t.image.blit(edge, [0, 0])
			if not right:
				t.image.blit(flip(edge), [0, 0])
		if not down:
			t.image.blit(ceiling, [0, 0])
			if not left:
				t.image.blit(underedge, [0, 0])
			if not right:
				t.image.blit(flip(underedge), [0, 0])
		
		self.tiles.append(t)

	def liquid(self, style, row , col):
		x = col * 40
		y = row * 40
		t = tile.Tile(x, y, 40, 40)
		t.image.set_colorkey([0, 0, 0])

		stillwater = pygame.transform.scale(self.cave[10][3], [40, 40])
		foamwater = pygame.transform.scale(self.cave[10][1], [40, 40])

		if style == "water":
			if row > 0 and self.layout[row - 1][col] == "f":
				t.image.blit(foamwater, [0, 0])
				t.animated = True
			else:
				t.image.blit(stillwater, [0, 0])

		self.liquids.append(t)

	def deco(self, style, row, col):
		x = col * 40
		y = row * 40
		t = tile.Tile(x, y, 40, 40)
		t.image.set_colorkey([0, 0, 0])

		drain = self.cave[8][0]
		nfall = self.cave[8][2]
		nfoam = self.cave[9][3]

		if style == "drain":
			t.image.blit(drain, [0, 0])
		if style == "narrow fall":
			if row < len(self.layout) - 1 and self.layout[row +  1][col] == "w":
				t.image.blit(nfoam, [0, 0])
				t.animated = True
			else:
				t.image.blit(nfall, [0, 0])

		self.backwalls.append(t)

	def do(self):
		self.framecounter += 1
		for cell in self.backwalls:
			cell.show(self.screen)
		for cell in self.tiles:
			cell.show(self.screen)

	def doLiquid(self):
		for cell in self.liquids:
			cell.show(self.screen)