# csp.py

from enum import Enum
import sys
import bag

class InputType(Enum):
	vars=1
	values=2
	limits=3
	unaryinc=4
	unaryexc=5
	binaryeq=6
	binarynoteq=7
	binarysimult=8

items = {}
bags = []
bag_min=0
bag_max=0
binaryequals = []
binarynotequals = []
un_incl = {}
un_excl = {}
bin_sim = {}
	
def parseInput(file):
	f = open(file, "r")
	input=0
	line = f.readline()
	
	while line:
		if line[0] is '#':
			input+=1
		else:
			line.split(" ")
			if type is 1:
				items[line[0]]=line[1] 
			elif type is 2:
				bags.append(Bag(line[0], line[1]))
			elif type is 3:
				bag_min = line[0]
				bag_max = line[1]
			elif type is 4:
				un_incl[line[0]]=line[:1]
			elif type is 5:
				un_excl[line[0]]=line[:1]
			elif type is 6:
				binaryequals.append(line[0]+line[1])
			elif type is 7:
				binarynotequals.append(line[0]+line[1])
			elif type is 8:
				bin_sim[line(0)+line(1)]=(line[2]+line[3])
		
		line = f.readline()
		
	f.close()


def within_limits(bg, n):
	return 


def can_be_in_bag(bg, x):
	return
	
if len(sys.argv) != 2:
	print("Proper usage is python csp.py inputfile")
	exit()
	
parseInput(sys.argv[1])

