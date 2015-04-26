#!/usr/bin/python


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
				print (map[i][y], end=" ")
				i=i+1;
			y=y+1;
			i = 0;
	print ("This is i: " + str(i) + " this is y: " + str(y))

def main():
	fillMapFromTextFile();

main()