from dik import Graph;
from dik import dijsktra;

# map = [[0 for col in range(101)] for row in range(101)]
mapSize =  101;
map = [ [0 for col in range(mapSize)] for row in range(mapSize)]
WIDTH = len(map) - 1
LENGTH = WIDTH
MAPFILE = "map.txt"
def main():

	# a = Graph();
	# a.add_node('a');
	# a.add_node('b');
	# a.add_node('c');
	# a.add_node('d');

	# a.add_edge('a', 'b', 1);
	# a.add_edge('a', 'd', 8);
	# a.add_edge('b', 'c', 1);
	# a.add_edge('c', 'd', 1);

	# a.add_edge('b', 'a', 1);
	# a.add_edge('d', 'a', 8);
	# a.add_edge('c', 'b', 1);
	# a.add_edge('d', 'c', 1);

	# solution = dijsktra(a, 'a');
	# print (solution);

	# print (" sdnfjdsf %s" %solution[0]);


	fillMapFromTextFile();
	g, start, end = buildGraph();

	visited, path = dijsktra(g, end );
	# print path

	# while the path is not at the end
	# if i give it the start it will give me the next node to get to end
	# path[start] != end
	print ;
	current = start
	while True:
		#figure out where to move
		if current == end:
			print 'Target found\n';
			break
		move = int(path[current]) - int(current) ; # current - north = WIDTH ; current - south = -WIDTH ; current - west = 1 ; current - east = 1
		if move == WIDTH:
			moveNorth();
		elif move == (-WIDTH):
			moveSouth();
		elif move == 1:
			moveWest();
		elif move == (-1):
			moveEast();
		current = path[current];

def moveNorth():
	print 'Move 1 unit North\n';
def moveSouth():
	print 'Move 1 unit south\n';
def moveWest():
	print 'Move 1 unit west\n';
def moveEast():
	print 'Move 1 unit east\n';

def buildGraph():
	start = '';
	g = Graph();
	# maps map[row][col] to graph[(row * WIDTH + col))]
	for row in range(LENGTH):  # length = 10, len(map) = 11. 11th value is \n. don't iterate through
		for col in range(WIDTH): 
			if map[row][col] == '2': 
				start = str(row * WIDTH + col);
				print 'found start found at row col: ', (row, col) 
				print 'found start at : %d' %(row * WIDTH + col)
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
if __name__ == "__main__": main()