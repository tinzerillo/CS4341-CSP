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
bag_min = 0
bag_max = 0
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
				print("type=3, line: ",line[1])
				bag_min = int(line[0])
				bag_max = int(line[1])
			elif type is 4:
				un_incl[line[0]]=line[1:]
			elif type is 5:
				un_excl[line[0]]=line[1:]
			elif type is 6:
				binaryequals.append(line[0]+line[1])
			elif type is 7:
				binarynotequals.append(line[0]+line[1])
			elif type is 8:
				bin_sim[line[0]+line[1]]=line[2]+line[3]
			line = f.readline()

	print("un_excl: ",un_excl)
	f.close()

def within_limits(bag, n):
	print("bag ",bag.name," currently contains ",len(bag.contains)," and we're trying to add ",n," to it")
	return len(bag.contains) + n <= bag_max and len(bag.contains) + n >= bag_min

def canAddToBag(item, bag):
	# unary exclusive
	if item in list(un_excl.keys()):
		if bag.name in un_excl[item]:
			return False

	# unary inclusive
	if item in list(un_incl.keys()):
		if bag.name not in un_incl[item]:
			return False

	# mutually exclusive
	for key in list(bin_sim.keys()):
		if key[0] is item and  bag.name in bin_sim[key]:
			if key[1] in bag.contains:
				return False
		elif key[1] is item and bag.name in bin_sim[key]:
			if key[0] in bag.contains:
				return False

	# binary not equals
	for pair in binarynotequals:
		if pair[0] is item and pair[1] in bag.contains:
			return False
		elif pair[1] is item and pair[0] in bag.contains:
			return False

	# fitting limits
	print("canAddToBag: bag_max is ", bag_max)
	global bag_max
	if bag_max is 0:
		return bag.capacity - bag.weight >= items[item]
	else:
		return within_limits(bag, 1)

def isCSPcomplete(assignment):

	print("isCSPcomplete: fit limits")

	# Fit limits
	for bag in assignment:
		if bag.weight >= (bag.capacity * 0.9):
			return False
		if within_limits(bag, 0) is False:
			return False

	print("isCSPcomplete: before unary inclusive")
	# Unary inclusive
	for constraint in un_incl.items():
		variable = constraint[0]
		# find what bag that variable is in...
		target_bag = None
		for bag in assignment:
			if variable in bag.contains:
				target_bag = bag
				break

		print("isCSPcomplete: inside un_incl")

		if target_bag not in constraint[1]:
			return False
		#else:
		#	return True

	#Unary exclusive

	print("len(un_excl) is ",len(un_excl))
	for constraint in un_excl.items():
		print("HELLO PRESTON",constraint)
		variable = constraint[0]
		# find what bag that variable is in...
		target_bag = None
		for bag in assignment:
			if variable in bag.contains:
				target_bag = bag
				break

		if target_bag in constraint[1]:
			return False
		#else:
		#	return True


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

	return min_remaining_var(variables, assignment)


def Backtrack(assignment, i):
	i -= 1
	if isCSPcomplete(assignment) is True or i is 0:
		return

	if len(nextUnassignedVariables(assignment)) is 0:
		return

	var = nextUnassignedVariables(assignment)

	for val in least_constraining_vals(var, assignment):
		if canAddToBag(var, val) is True:
			val.addItem(var, items[var])
			break;

	if nextUnassignedVariables(assignment) is not []:
		Backtrack(assignment, i)


def min_remaining_var(items, bags):
	bags_per_item = {}

	for i in items:
		bags_per_item[i] = 0
		for b in bags:
			if canAddToBag(i, b):
				bags_per_item[i] += 1
		
	return min(bags_per_item, key=bags_per_item.get)

def least_constraining_vals(items, bags):
	items_per_bag = {}

	for b in bags:
		items_per_bag[b] = 0
		for i in items:
			if canAddToBag(i, b):
				items_per_bag[b] += 1
	
	#Flip dictionary
	sortedDict = sorted(items_per_bag, key=items_per_bag.get)
	return reversed(sortedDict)
	

	
def arc_consistency():
	pass


def output(assignment):
	for bag in assignment:
		print(bag.name, " ", end="")
		for variable in bag.contains:
			print(variable, end=" ")
		print(" ")

		print("number of items: " + str(len(bag.contains)))
		print("total weight: " + str(bag.weight) + "/" + str(bag.capacity))
		print("wasted capacity: " + str(bag.wastedCapacity()))
		print("")


if len(sys.argv) != 2:
	print("Proper usage is python csp.py inputfile")
	exit()


i = 200
parseInput(sys.argv[1])
Backtrack(bags, i)

output(bags)
