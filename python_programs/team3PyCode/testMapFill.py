#!/usr/bin/python
import pygame, time


map = [[0 for col in range(101)] for row in range(101)]



def fillMapFromTextFile():
	mapFileLocation = "map.txt";
	i = 0;
	y = 0;
	with open(mapFileLocation) as f:
		for line in f:
			list = line.split(',');
			for item in list:
				map[i][y] = item;
				print (map[i][y]),
				i=i+1;
			y=y+1;
			i = 0;
	print ("This is i: " + str(i) + " this is y: " + str(y))


def testPlayAudioFile():
	file = 'forward.wav'
	pygame.init()
	pygame.mixer.init(48000, -16, 1, 1024)
	pygame.mixer.music.load(file)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		continue


def main():
	#fillMapFromTextFile();
	testPlayAudioFile();

main()
