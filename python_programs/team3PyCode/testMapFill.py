#!/usr/bin/python
import time, wave, pymedia.audio.sound as sound


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
	f= wave.open( 'forward.wav', 'rb' )
	sampleRate= f.getframerate()
	channels= f.getnchannels()
	format= sound.AFMT_S16_LE
	snd= sound.Output( sampleRate, channels, format )
	s= f.readframes( 300000 )
	snd.play( s )
	while snd.isPlaying(): time.sleep( 0.005 )


def main():
	#fillMapFromTextFile();
	testPlayAudioFile();

main()