import pygame, sys, random
from pygame.locals import *

# Constants
GRIDWIDTH = 5  # number of columns in the grid
GRIDHEIGHT = 5 # number of rows in the grid
CELLSIZE = 68  # size of each cell in the grid
WINDOWWIDTH = 640
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
CONTROLPANELCOLOR = DARKBLUE
TEXTCOLOR = WHITE
BASICFONTSIZE = 20

# Button colors
BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = DARKBLUE

# Margins
XMARGIN = int((WINDOWWIDTH - CONTROLPANELWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# Directions
NORTH = 'north'
NORTHEAST = 'northeast'
EAST = 'east'
SOUTHEAST = 'southeast'
SOUTH = 'south'
SOUTHWEST = 'southwest'
WEST = 'west'
NORTHWEST = 'northwest'

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, 
			RUN_SURF, RUN_RECT, 
			SPEED_UP_SURF, SPEED_UP_RECT, 
			SPEED_LABEL_SURF, SPEED_LABEL_RECT, 
			SPEED_DOWN_SURF, SPEED_DOWN_RECT, 
			STEP_UP_SURF, STEP_UP_RECT, 
			STEP_LABEL_SURF, STEP_LABEL_RECT, 
			STEP_DOWN_SURF, STEP_DOWN_RECT
	
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
	SPEED_DOWN_SURF, SPEED_DOWN_RECT = makeText(' - ', TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 300, 80)

	# Step controls
	STEP_UP_SURF, STEP_UP_RECT = makeText(' + ', BUTTONTEXTCOLOR, BUTTONCOLOR, WINDOWWIDTH - 100, 160)
	STEP_LABEL_SURF, STEP_LABEL_RECT = makeText('Step', TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 200, 160)
	STEP_DOWN_SURF, STEP_DOWN_RECT = makeText(' - ', TEXTCOLOR, BGCOLOR, WINDOWWIDTH - 300, 160)

	# Generate a random grid configuration
	grid = generateGrid()
	# Create an empty list to store steps for forward and backward stepping
	allSteps = []

	# Main game loop
	# while True:
		# LOGIC ...