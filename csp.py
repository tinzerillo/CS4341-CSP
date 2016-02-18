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
	return bag.weight + n <= bag_max and bag.weight + n >= bag_min

def canAddToBag(item, bag):
	# unary exclusive
	if item in un_excl.keys():
		if bag in un_excl[item]:
			return False
			
	# unary inclusive
	if item in un_incl.keys():
		if bag not in un_incl[item]:
			return False
			
	# mutually exclusive
	for key in list(bin_sim.keys()):
		if key[0] is item and  bag in bin_sim[key]:
			if key[1] in bag.contains:
				return False
		elif key[1] is item and bag in bin_sim[key]:
			if key[0] in bag.contains:
				return False
				
	# binary not equals
	for pair in binarynotequals:
		if pair[0] is item and pair[1] in bag.contains:
			return False
		elif pair[1] is item and pair[0] in bag.contains:
			return False
	
	# fitting limits
	if bag_max is 0:
		return bag.capacity - bag.weight >= items[item]
	else:
		return within_limits(bag, items[item])

def isCSPcomplete(assignment):

	# Fit limits
	for bag in assignment:
		if bag.count < (bag.capacity * 0.9):
			return False
		if within_limits(bag, bag.count) is False:
			return False

	# Unary inclusive
	for constraint in un_incl.items():
		variable = constraint[0]
		# find what bag that variable is in...
		target_bag = None
		for bag in assignment:
			if variable in bag.contains:
				target_bag = bag
				break

		if target_bag not in constraint[1]:
			return False
		else:
			return True

	#Unary exclusive

	for constraint in un_excl.items():
		variable = constraint[0]
		# find what bag that variable is in...
		target_bag = None
		for bag in assignment:
			if variable in bag.contains:
				target_bag = bag
				break

		if target_bag in constraint[1]:
			return False
		else:
			return True


	#Binary constraints

		#Equal
	for constraint in binaryequals.items():
		variableOne = constraint[0][1]
		variableTwo = constraint[0][1]


		for bag in assignment:
			if variableOne in bag.contains:
				if variableTwo not in bag.contains:
					return False


	#Not equal
	for constraint in binarynotequals.items():
		variableOne = constraint[0][1]
		variableTwo = constraint[0][1]

		for bag in assignment:
			if variableOne in bag.contains:
				if variableTwo in bag.contains:
					return False


	#Binary simultaneous
	for constraint in bin_sim.items():
		variableOne = constraint[0][0]
		variableTwo = constraint[0][1]

		bagOne = constraint[1][0]
		bagTwo = constraint[1][1]

		bagOneClass = None
		bagTwoClass = None

		for bag in assignment:
			if bag.name == bagOne:
				bagOneClass = bag
			elif bag.name == bagTwo:
				bagTwoClass = bag

		if variableOne in bagOneClass.contains and variableTwo not in bagTwoClass.contains:
			return False

		if variableOne in bagTwoClass.contains and variableTwo not in bagOneClass.contains:
			return False

		if variableTwo in bagOneClass.contains and variableOne not in bagTwoClass.contains:
			return False

		if variableTwo in bagTwoClass.contains and variableOne not in bagOneClass.contains:
			return False

	return True

def nextUnassignedVariables(assignment):
	#assignment: [] of bags
	variables = list(items.keys())

	for b in assignment:
		for variable in b.contains:
			if variable in variables:
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
			Backtrack(assignment)

def min_remaining_vals():
	pass
	
def least_constraining_val():
	pass
	
def arc_consistency():
	pass
			
			
if len(sys.argv) != 2:
	print("Proper usage is python csp.py inputfile")
	exit()

parseInput(sys.argv[1])
Backtrack(bags)
#for b in bags:
	#print(b.contains)
