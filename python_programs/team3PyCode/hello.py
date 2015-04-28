from dik import Graph;
from dik import dijsktra;

# map = [[0 for col in range(101)] for row in range(101)]
map = [ [0 for col in range(11)] for row in range(11)]
WIDTH = 10
LENGTH = WIDTH
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
	# i have the file in a 2d array
	# translate data into graph
	start = '';
	g = Graph();
	for row in range(LENGTH):
		for col in range(WIDTH):
			if map[row][col] == '2': 
				start = str(row + WIDTH * col);
				print 'found start found at row col: ', (row, col) 
				print 'found start at : %d' %(row * WIDTH + col)
			if map[row][col] == '3': 
				end = str(row + WIDTH * col);
				print 'found end at ' , (row, col)
			if map[row][col] != '7' :
				# send to graph
				# create node
				node = str( row + WIDTH * col)
				g.add_node( node )
				# create north neighbor
				if row != 0: # not the first row
					northNode = str( (row-1) + WIDTH * col ) #northern neighbor
					if map[row-1][col] != '7':
						g.add_edge(node, northNode, 1)
						g.add_edge(northNode, node, 1) # dijkstras alg requires bidirectional edges						
				# create south neighbor
				# create east neighbor
				# create west neighbor
				if col != 0: # edge case for west
					if map[row][col-1] != '7':
						westNode = str( (row)+ WIDTH * (col-1))
						g.add_edge(node, westNode, 1)
						g.add_edge(westNode, node, 1)  #only do these nodes because east and south nodes have not been read yet. unknow results if you assign edge to unknown node

	solution = dijsktra(g, end );
	print solution
	# print a;

	# be able to access graph

def fillMapFromTextFile():
	mapFileLocation = "testmap.txt";
	i = 0;
	y = 0;
	with open(mapFileLocation) as f:
		for line in f:
			list = line.split(',');
			for item in list:
				map[i][y] = item;
				i=i+1;
			y=y+1;
			i = 0;
if __name__ == "__main__": main()