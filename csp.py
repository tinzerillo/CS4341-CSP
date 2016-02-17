# csp.py

from enum import Enum
import sys
from bag import *

class InputType(Enum):
	vars=1
	values=2
	limits=3
	unaryinc=4
	unaryexc=5
	binaryeq=6
	binarynoteq=7
	binarysimult=8

# constraints 
items = {}
bag_min=0
bag_max=0
binaryequals = []
binarynotequals = []
un_incl = {}
un_excl = {}
bin_sim = {}

bags = []
	
def parseInput(file):
	f = open(file, "r")
	type=0
	line = f.readline()
	
	while line:
		if line[0] is '#':
			type+=1
			line = f.readline()
		else:
			line = line.rstrip().split(" ")
			if type is 1:
				items[line[0]]=int(line[1])
			elif type is 2:
				bags.append(Bag(line[0], int(line[1])))
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
				bin_sim[line[0]+line[1]]=line[2]+line[3]
			line = f.readline()
		
	f.close()


def within_limits(bag, n):
	return bag.count() < n
	
def canAddToBag(item, bag):
	if bag_max is 0:
		return bag.capacity >= items[item]
	else:
		return within_limits(bag, items[item])
	
def isCSPcomplete(assignment):
	return False

def nextUnassignedVariables(assignment):
	#assignment: [] of bags
	variables = list(items.keys())
	
	for bag in assignment:
		for variable in bag.contains:
			variables.remove(variable)
		if len(variables) is 0:
			return []
			
	return variables	

def Backtrack(assignment):
	if isCSPcomplete is True:
		return 
	
	if len(nextUnassignedVariables(assignment)) is 0:
		return
		
	var = nextUnassignedVariables(assignment)[0]
		
	for bag in assignment:
		if canAddToBag(var, bag) is True:
			bag.addItem(var, items[var])
		else:
			i+=1
			Backtrack(assignment)
	
if len(sys.argv) != 2:
	print("Proper usage is python csp.py inputfile")
	exit()
	
parseInput(sys.argv[1])
Backtrack(bags)
for b in bags:
	print(b.contains)
	

