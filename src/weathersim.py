# LOGIC ...
# Algorithm:
# 	Get events
#	if event == mouse_button_up:
#		if (spotx, spoty) == (None, None):
#			if run_rect.collide:
#				if state == pause: state = play
#				elif state == play: state = pause
#			elif speed_up_rect.collide:
#				increaseFPS()
#			elif speed_down_rect.collide:
#				decreaseFPS()
#			elif step_up_rect.collide:
#				nextStep()
#			elif step_down_rect.collide:
#				prevStep()
#	elif event == QUIT:
#		pygame.quit()
#		sys.exit()
#	if state == play:
#		runSim()
#	elif state == pause:
#		stopSim()
#
#	Functions:
#		makeText()
#		generateGrid()
#		getSpotClicked()
#		increaseFPS()
#		decreaseFPS()
#		nextStep()
#		prevStep()
#		runSim()
#		stopSim()
import pygame, sys, random
from pygame.locals import *

# Constants
GRIDWIDTH = 85  # number of columns in the grid
GRIDHEIGHT = 85 # number of rows in the grid
CELLSIZE = 4  # size of each cell in the grid (340 / GRIDWIDTH)
WINDOWWIDTH = 800
WINDOWHEIGHT = 480
CONTROLPANELWIDTH = 300
FPS = 30

# Colors     R    G    B
BLACK =    (  0,   0,   0)
GRAY =     (128, 128, 128)
WHITE =    (255, 255, 255)
RED =      (255,   0,   0)
YELLOW =   (255, 255,   0)
GREEN =    (  0, 255,   0)
CYAN =     (  0, 255, 255)
BLUE =     (  0,   0, 255)
DARKBLUE = (  3,  54,  73)

# Overall colors and fontsize
BGCOLOR = BLACK
LINECOLOR = GRAY
CELLCOLOR = BLACK
CONTROLPANELCOLOR = DARKBLUE
TEXTCOLOR = WHITE
BASICFONTSIZE = 20

# Button colors
BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = DARKBLUE

# Temperature colors
TEMPERATURE = [RED, GREEN, BLUE]

# Margins
XMARGIN = int((WINDOWWIDTH - CONTROLPANELWIDTH - (CELLSIZE * GRIDWIDTH + (GRIDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (CELLSIZE * GRIDHEIGHT + (GRIDHEIGHT - 1))) / 2)

# Directions
NORTH = 'north'
NORTHEAST = 'northeast'
EAST = 'east'
SOUTHEAST = 'southeast'
SOUTH = 'south'
SOUTHWEST = 'southwest'
WEST = 'west'
NORTHWEST = 'northwest'

# State (Play/Pause)
PLAY = 'play'
PAUSE = 'pause'

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, RUN_SURF, RUN_RECT, SPEED_UP_SURF, SPEED_UP_RECT, SPEED_LABEL_SURF, SPEED_LABEL_RECT, SPEED_DOWN_SURF, SPEED_DOWN_RECT, STEP_UP_SURF, STEP_UP_RECT, STEP_LABEL_SURF, STEP_LABEL_RECT, STEP_DOWN_SURF, STEP_DOWN_RECT
	
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Weather Sim')
	BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

	# Control panel buttons
	# Run button
	RUN_SURF, RUN_RECT = makeText('Run', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 160, 0)

	# Speed controls
	SPEED_UP_SURF, SPEED_UP_RECT = makeText(' + ', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 100, 80)
	SPEED_LABEL_SURF, SPEED_LABEL_RECT = makeText('Speed', TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 200, 80)
	SPEED_DOWN_SURF, SPEED_DOWN_RECT = makeText(' - ', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 250, 80)

	# Step controls
	STEP_UP_SURF, STEP_UP_RECT = makeText(' + ', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 100, 160)
	STEP_LABEL_SURF, STEP_LABEL_RECT = makeText('Step', TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 200, 160)
	STEP_DOWN_SURF, STEP_DOWN_RECT = makeText(' - ', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 250, 160)

	# Generate a random starting grid configuration
	# Create an empty list to store steps for forward and backward stepping
	# Stores grid configurations
	mainGrid, allSteps, lastStep = generateGrid()
	stepCount = 0
	state = PAUSE

	while True:
		drawGrid(mainGrid)

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				spotx, spoty = getSpotClicked(mainGrid, event.pos[0], event.pos[1])

				if (spotx, spoty) == (None, None):
					if RUN_RECT.collidepoint(event.pos):
						if state == PAUSE:
							state = PLAY
							print('state switched to play')
						elif state == PLAY:
							state = PAUSE
							print('state switched to pause')
		# 			elif SPEED_UP_RECT.collidepoint(event.pos):
		# 				increaseFPS()
		# 			elif SPEED_DOWN_RECT.collidepoint(event.pos):
		# 				decreaseFPS()
					elif STEP_UP_RECT.collidepoint(event.pos):
						print('nextStep button hit')
						mainGrid, allSteps, stepCount = nextStep(mainGrid, allSteps, stepCount)
					elif STEP_DOWN_RECT.collidepoint(event.pos):
						print('prevStep button hit')
						print('stepCount' + str(stepCount))
						print(str(allSteps))
						if stepCount > 1:
							mainGrid, allSteps, stepCount = prevStep(mainGrid, allSteps, stepCount)
					# elif RESET_RECT.collidepoint(event.pos):
					# 	print('reset button hit')
					# 	reset(mainGrid, allSteps, stepCount)
			elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
		if state == PLAY:
			mainGrid, allSteps, stepCount, state = runSim(mainGrid, allSteps, stepCount, state)

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def runSim(grid, allSteps, stepCount, state):
	while state == PLAY:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				spotx, spoty = getSpotClicked(grid, event.pos[0], event.pos[1])
				if (spotx, spoty) == (None, None):
					if RUN_RECT.collidepoint(event.pos):
						print('state switched to pause')
						state = PAUSE
			elif event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
		grid, allSteps, stepCount = nextStep(grid, allSteps, stepCount)
	return grid, allSteps, stepCount, state

def nextStep(grid, allSteps, stepCount):
	for x in range(GRIDWIDTH):
		for y in range(GRIDHEIGHT):
			current = grid[x][y]
			surrounding = getSurroundingCells(grid, x, y)
			numBlue = surrounding.count(BLUE)
			numGreen = surrounding.count(GREEN)
			numRed = surrounding.count(RED)

			grid[x][y] = findNextColor(current, numRed, numGreen, numBlue)
	allSteps.append(grid)
	stepCount += 1
	drawGrid(grid)
	pygame.display.update()
	pygame.time.wait(500)
	return grid, allSteps, stepCount

def prevStep(grid, allSteps, stepCount):
	allSteps = allSteps[:-1]
	stepCount -= 1
	grid = allSteps[-1]
	drawGrid(grid)
	pygame.display.update()
	pygame.time.wait(500)
	return grid, allSteps, stepCount

def findNextColor(current, R, G, B):
	if current == RED:
		if R > G+B:
			if G > B:
				return RED
			else:
				return GREEN
		elif G > R+B:
			if R > B:
				return RED
			else:
				return GREEN
		elif B > R+G:
			return GREEN
			# if R > G:
			# 	return GREEN
			# else:
			# 	return BLUE
		else:
			return random.choice([RED, GREEN])
	elif current == GREEN:
		if R > G+B:
			if G > B:
				return RED
			else:
				return GREEN
		elif G > R+B:
			if R > B:
				return RED
			else:
				return BLUE
		elif B > R+G:
			if R > G:
				return GREEN
			else:
				return BLUE
		else:
			return random.choice([RED, GREEN, BLUE])
	elif current == BLUE:
		if R > G+B:
			return GREEN
			# if G > B:
			# 	return GREEN
			# else:
			# 	return BLUE
		elif G > R+B:
			if R > B:
				return GREEN
			else:
				return BLUE
		elif B > R+G:
			if R > G:
				return GREEN
			else:
				return BLUE
		else:
			return random.choice([GREEN, BLUE])

def getSurroundingCells(grid, x, y):
	surrounding = []
	if x-1 > 0:
		surrounding.append(grid[x-1][y])
	if x+1 < GRIDWIDTH:
		surrounding.append(grid[x+1][y])
	if y-1 > 0:
		surrounding.append(grid[x][y-1])
	if y+1 < GRIDHEIGHT:
		surrounding.append(grid[x][y+1])
	if x-1 > 0 and y-1 > 0:
		surrounding.append(grid[x-1][y-1])
	if x-1 > 0 and y+1 < GRIDHEIGHT:
		surrounding.append(grid[x-1][y+1])
	if x+1 < GRIDWIDTH and y-1 > 0:
		surrounding.append(grid[x+1][y-1])
	if x+1 < GRIDWIDTH and y+1 < GRIDHEIGHT:
		surrounding.append(grid[x+1][y+1])

	return surrounding

def makeText(text, color, bgcolor, top, left):
	# Create the Surface and Rect objects for some text
	textSurf = BASICFONT.render(text, True, color, bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (top, left)
	return (textSurf, textRect)

def getStartingGrid():
	# Return a grid data structure that is blank
	grid = []
	for x in range(GRIDWIDTH):
		column = []
		for y in range(GRIDHEIGHT):
			column.append(BLACK)
		grid.append(column)
	return grid

def drawGrid(grid):
	DISPLAYSURF.fill(BGCOLOR)
	for cellX in range(len(grid)):
		for cellY in range(len(grid[0])):
			if grid[cellX][cellY]:
				drawCell(cellX, cellY, grid[cellX][cellY])
	
	left, top = getLeftTopOfCell(0, 0)
	width = GRIDWIDTH * CELLSIZE
	height = GRIDHEIGHT * CELLSIZE

	DISPLAYSURF.blit(RUN_SURF, RUN_RECT)

	DISPLAYSURF.blit(SPEED_UP_SURF, SPEED_UP_RECT)
	DISPLAYSURF.blit(SPEED_LABEL_SURF, SPEED_LABEL_RECT)
	DISPLAYSURF.blit(SPEED_DOWN_SURF, SPEED_DOWN_RECT)

	DISPLAYSURF.blit(STEP_UP_SURF, STEP_UP_RECT)
	DISPLAYSURF.blit(STEP_LABEL_SURF, STEP_LABEL_RECT)
	DISPLAYSURF.blit(STEP_DOWN_SURF, STEP_DOWN_RECT)

def drawCell(cellX, cellY, color, adjx=0, adjy=0):
	left, top = getLeftTopOfCell(cellX, cellY)
	pygame.draw.rect(DISPLAYSURF, color, (left + adjx, top + adjy, CELLSIZE, CELLSIZE))

def getLeftTopOfCell(cellX, cellY):
	left = XMARGIN + (cellX * CELLSIZE) + (cellX - 1)
	top = YMARGIN + (cellY * CELLSIZE) + (cellY - 1)
	return (left, top)

def getSpotClicked(grid, x, y):
	# From the x, y pixel coords, get the x, y grid coords
	for cellX in range(len(grid)):
		for cellY in range(len(grid[0])):
			left, top = getLeftTopOfCell(cellX, cellY)
			cellRect = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
			if cellRect.collidepoint(x, y):
				return (cellX, cellY)
	return (None, None)

def generateGrid():
	allSteps = []
	grid = getStartingGrid()
	drawGrid(grid)
	pygame.display.update()
	pygame.time.wait(500)
	lastStep = None
	for x in range(GRIDWIDTH):
		for y in range(GRIDHEIGHT):
			grid[x][y] = random.choice(TEMPERATURE)
	
	drawGrid(grid)
	pygame.display.update()
	pygame.time.wait(500)

	return grid, allSteps, lastStep

if __name__ == '__main__':
	main()