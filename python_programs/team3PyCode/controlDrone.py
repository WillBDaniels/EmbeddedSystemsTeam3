#!/usr/bin/python


# Import required Python libraries
import time
import RPi.GPIO as GPIO

import pygame

import libardrone

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)



# Define GPIO to use on Pi
GPIO_TRIGGER_FRONT = 17
GPIO_ECHO_FRONT = 18
GPIO_TRIGGER_RIGHT = 22
GPIO_ECHO_RIGHT = 23
GPIO_TRIGGER_LEFT = 6
GPIO_ECHO_LEFT = 12
map = [[0 for col in range(101)] for row in range(101)]

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
	print "trying to takeoff"
	drone.takeoff()
	print "should have taken off"
	drone.hover()
	#drone.reset()
	while 1==1:
		distanceFront = setupUltrasonic(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT)
		distanceLeft = setupUltrasonic(GPIO_TRIGGER_LEFT, GPIO_ECHO_LEFT)
		distanceRight = setupUltrasonic(GPIO_TRIGGER_RIGHT, GPIO_ECHO_RIGHT)
		

		if distanceFront < 50:
            #we would be here if we had a drone
	    #drone.halt
	    if (distanceLeft > 50):
	    	handleObstacleLeft()
		elif (distanceRight > 50):
			handleObstacleRight()
		elif ((distanceRight < 50) & (distanceLeft < 50) & (distanceFront < 50)):
			print "drone is in a location it can't navigate out of, landing..."
			handleLandDrone()
		#break;
		else:
			handleObstacleFront()
	    
	#drone.halt

	print "distanceFront: %f, distanceleft: %f, distanceRight: %f" % (distanceFront, distanceLeft, distanceRight)
# Reset GPIO settings
	GPIO.cleanup()
def handleLandDrone():
	print "Drone is stopping"


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
	mapFileLocation = "map.txt";
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






