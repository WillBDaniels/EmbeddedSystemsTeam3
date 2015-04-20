#!/usr/bin/python


# Import required Python libraries
import time
import RPi.GPIO as GPIO

import pygame

import libardrone

# Use BCM GPIO references
# instead of physical pin numbers


from dik import Graph;
from dik import dijsktra;

# map = [[0 for col in range(101)] for row in range(101)]
mapSize =  101;
map = [ [0 for col in range(mapSize)] for row in range(mapSize)]
WIDTH = len(map) - 1
LENGTH = WIDTH
currentCol = 0;
currentRow = 0;
MAPFILE = "map.txt"
GPIO.setmode(GPIO.BCM)



# Define GPIO to use on Pi
GPIO_TRIGGER_FRONT = 17
GPIO_ECHO_FRONT = 18
GPIO_TRIGGER_RIGHT = 22
GPIO_ECHO_RIGHT = 23
GPIO_TRIGGER_LEFT = 6
GPIO_ECHO_LEFT = 12

print "Ultrasonic Measurement"


def main():
	fillMapFromTextFile()
	print "In the main method"
	W, H = 320, 240
	drone = libardrone.ARDrone()
	running = True
	print "drone is running, should be working"
#while running:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
#        elif event.type == pygame.KEYUP:
#            drone.hover()
#        elif event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_ESCAPE:
#                drone.reset()
#                running = False
#            # takeoff / land
#            elif event.key == pygame.K_RETURN:
#                drone.takeoff()
#            elif event.key == pygame.K_SPACE:
#                drone.land()
#            # emergency
#            elif event.key == pygame.K_BACKSPACE:
#               drone.reset()
#           # forward / backward
#            elif event.key == pygame.K_w:
#                drone.move_forward()
#            elif event.key == pygame.K_s:
#                drone.move_backward()
#            # left / right
#            elif event.key == pygame.K_a:
#                drone.move_left()
#            elif event.key == pygame.K_d:
#                drone.move_right()
#            # up / down
#           elif event.key == pygame.K_UP:
#               drone.move_up()
#           elif event.key == pygame.K_DOWN:
#              drone.move_down()
#          # turn left / turn right
#          elif event.key == pygame.K_LEFT:
#              drone.turn_left()
#          elif event.key == pygame.K_RIGHT:
#              drone.turn_right()
#          # speed
	#This is how you get the raw data from the drone. Coolio.
	#drone.navdata will get the actual raw data. drone.navdata
	print "trying to takeoff"
	drone.takeoff()
	print "should have taken off"
	drone.hover()

	fillMapFromTextFile();
	g, start, end = buildGraph();

	visited, path = dijsktra(g, end );
    #<--------Perform diagnostics on drone, things like lateral/up/down drift, and then pre-program in compensation moves for how it tends to drift.
    # aka: if the drone tends to list to the left a little, then we should time that, and every iteration of the loop should account for this.
    # We then need to save this value into a file with a unique UUID of the drone, so that upon future runs, we don't need to keep re-calibrating the drone.
    # the calibration should skip if the ID already exists.
	#drone.reset()
	while 1==1:
		#figure out where to move
		if current == end:
			handleLandDrone();
			print 'Target found\n';
			break
		move = int(path[current]) - int(current) ; # current - north = WIDTH ; current - south = -WIDTH ; current - west = 1 ; current - east = 1
		distList = distanceLogic(getDistances())
		if move == WIDTH:
			if (distList[0] == 1):
				moveNorth(false);
			elif(distList[1] == 1):
				moveWest(true);
			elif (distList[2] == 1):
				moveEast(true);
			elif (distlist[3] != -999):
				moveSouth(true);
			else:
				handleLandDrone();
		elif move == (-WIDTH):
			if (distList[3] != -999):
				moveSouth(false);
			elif(distList[1] == 1):
				moveWest(true);
			elif (distList[2] == 1):
				moveEast(true);
			elif (distlist[0] == 1):
				moveNorth(true);
			else:
				handleLandDrone();
		elif move == 1:
			if (distList[1] == 1):
				moveNorth(false);
			elif(distList[0] == 1):
				moveWest(true);
			elif (distList[2] == 1):
				moveEast(true);
			elif (distlist[3] != -999):
				moveSouth(true);
			else:
				handleLandDrone();
		elif move == (-1):
			if (distList[2] == 1):
				moveNorth(false);
			elif(distList[1] == 1):
				moveWest(true);
			elif (distList[0] == 1):
				moveEast(true);
			elif (distlist[3] != -999):
				moveSouth(true);
			else:
				handleLandDrone();
		current = path[current];
		drone.halt()
# Reset GPIO settings
	GPIO.cleanup()



def getDistances():
	distanceFront = setupUltrasonic(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT)
	distanceLeft = setupUltrasonic(GPIO_TRIGGER_LEFT, GPIO_ECHO_LEFT)
	distanceRight = setupUltrasonic(GPIO_TRIGGER_RIGHT, GPIO_ECHO_RIGHT)
	return distanceFront, distanceLeft, distanceRight

def distanceLogic(distFront, distLeft, distRight):
	minDistance = 75
	distList = [-1, -1, -1]
	if ((distanceFront < minDistance) && (map[currentRow - 1][currnentCol] != 7)):
		distList[0] = -1
            #we would be here if we had a drone
    #drone.halt
    elif ((distanceLeft > minDistance)  && (map[currentRow][currnentCol - 1] != 7)):
    	distList[1] = 1;
	elif ((distanceRight > minDistance) && (map[currentRow][currnentCol + 1] != 7)):
		distList[2] = 1;
	elif ((distanceRight < minDistance) & (distanceLeft < minDistance) & (distanceFront < minDistance)):
		print "drone is in a location it can't navigate out of, landing..."
		distList[3] = -999;
	#break;
	else:
		distList[0] = 1;
	return distList;

def moveNorth(didGetDiverted):
	print 'Move 1 unit North\n';
	currentCol -= 1
	if (didGetDiverted):
		map[row][col] = 2;
		buildGraph()
	handleObstacleFront();
def moveSouth(didGetDiverted):
	handleObstacleBack();
	currentCol += 1
	if (didGetDiverted):
		map[row][col] = 2;
		buildGraph()

	print 'Move 1 unit south\n';
def moveWest(didGetDiverted):
	handleObstacleLeft()
	currentRow -= 1
	if (didGetDiverted):
		map[row][col] = 2;
		buildGraph()
	print 'Move 1 unit west\n';
def moveEast(didGetDiverted):
	handleObstacleRight();
	currentRow += 1
	if (didGetDiverted):
		map[row][col] = 2;
		buildGraph()
	print 'Move 1 unit east\n';

def buildGraph():
	start = '';
	g = Graph();
	# maps map[row][col] to graph[(row * WIDTH + col))]
	for row in range(LENGTH):  # length = 10, len(map) = 11. 11th value is \n. don't iterate through
		for col in range(WIDTH):
			if map[row][col] == '2':
				start = str(row * WIDTH + col);
				currentCol = col;
				currentRow = row;
				print 'found start found at row col: ', (row, col)
				print 'found start at : %d' %(row * WIDTH + col)
				#reset the start value so that we can re-assign the start later.
				map[row][col] = '0';

			if map[row][col] == '3':
				end = str(row * WIDTH + col);
				print 'found end at ' , (row, col)
			if map[row][col] != '7' : # wont include 7 nodes because done can't fly there.
				# send to graph
				# create node
				node = str( row * WIDTH + col)
				g.add_node( node )
				# create edge (north neighbor)
				if row != 0: # the first row doesn't have north neighbor; assumed row != 7
					northNode = str( (row-1) * WIDTH + col ) #northern neighbor
					if map[row-1][col] != '7': #accounts for maps with curves
						g.add_edge(node, northNode, 1)
						g.add_edge(northNode, node, 1) # dijkstras alg requires bidirectional edges
				# create south neighbor ; not needed, done by (row, col+1) node
				# create east neighbor  ; not needed, done by (row, col+1) node
				# create west neighbor
				if col != 0: # edge case for west
					if map[row][col-1] != '7':
						westNode = str( (row) * WIDTH + (col-1))
						g.add_edge(node, westNode, 1)
						g.add_edge(westNode, node, 1)  #only do these nodes because east and south nodes have not been read yet. unknow results if you assign edge to unknown node
	return g, start, end;
	    
	#drone.halt
def handleLandDrone():
	print "Drone is stopping"
	#playAudioFile("stop.wav"); <----------- We still need this audio clip.


def handleObstacleLeft():
	#drone.move_left()
	print "drone moving left for 3 second..."
	playAudioFile("left.wav")
	time.sleep(3)
def handleObstacleRight():
	print "drone moving right for 3 second..."
	playAudioFile("right.wav")
	time.sleep(3)
def handleObstacleFront():
	print "drone moving Forward for 3 second..."
	playAudioFile("forward.wav")
	time.sleep(3)

def handleObstacleBack():
	print "drone moving Backward for 3 seconds...";
	#playAudioFile("back.wav") < ---- we still need this audio clip.
	time.sleep(3)
   
def setupUltrasonic(TRIGGER, ECHO):
	# Set pins as output and input
	GPIO.setup(TRIGGER,GPIO.OUT)  # Trigger
	GPIO.setup(ECHO,GPIO.IN)      # Echo

	# Set trigger to False (Low)
	GPIO.output(TRIGGER, False)

	# Allow module to settle
	time.sleep(0.5)

	# Send 10us pulse to trigger
	GPIO.output(TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(TRIGGER, False)
	start = time.time()
	while GPIO.input(ECHO)==0:
		start = time.time()

	while GPIO.input(ECHO)==1:
		stop = time.time()

	# Calculate pulse length
		elapsed = stop-start

	# Distance pulse travelled in that time is time
	#	 multiplied by the speed of sound (cm/s)
		distance = elapsed * 34000

	# That was the distance there and back so halve the value
		distance = distance / 2

	return distance


def playAudioFile(audioFileName):
	file = audioFilename
	pygame.init()
	pygame.mixer.init(48000, -16, 1, 1024)
	pygame.mixer.music.load(file)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		continue

def fillMapFromTextFile():
	mapFileLocation = MAPFILE;
	i = 0;
	y = 0;
	with open(mapFileLocation) as f:
		for line in f:
			list = line.split(',');
			for item in list:
				map[y][i] = item;
				i=i+1;
			y=y+1;
			i = 0;

main()






