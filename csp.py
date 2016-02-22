# Project 5 - CSP
# Theresa Inzerillo & Preston Mueller
# CS4341 Introduction to Artificial Intelligence
#
# This class implements a backtrack algorithm on
# constraints, items and bags given in an input file.
#
# To run: python csp.py [inputfile]

from enum import Enum
from constraint import Constraint
import sys
from bag import *
import math

class InputType(Enum):
	vars=1
	values=2
	limits=3
	unaryinc=4
	unaryexc=5
	binaryeq=6
	binarynoteq=7
	binarysimult=8


# Parses a file into a constraint object
#
# @param file - filename to open
def parseInput(file):
	try:
		f = open(file, "r")
	except FileNotFoundError as e:
		print("Error: could not find", file)
		sys.exit(1)
	
	type=0
	line = f.readline()

	while line:
		if line[0] is '#':
			type += 1
			line = f.readline()
		else:
			line = line.rstrip().split(" ")
			if type is 1:
				items[line[0]]=int(line[1])
			elif type is 2:
				bags.append(Bag(line[0], int(line[1])))
			elif type is 3:
				constraints.bag_min = int(line[0])
				constraints.bag_max = int(line[1])
			elif type is 4:
				constraints.un_incl[line[0]]=line[1:]
			elif type is 5:
				constraints.un_excl[line[0]]=line[1:]
			elif type is 6:
				constraints.binaryequals.append(line[0]+line[1])
			elif type is 7:
				constraints.binarynotequals.append(line[0]+line[1])
			elif type is 8:
				constraints.bin_sim[line[0]+line[1]]=line[2]+line[3]
			line = f.readline()

	f.close()

	
# N=0: checks if bag satisfies fitting limites
# N=1: checks if adding an item will satisfy fitting limits
#
# @param bag - the bag to check
# @param n - the number of items to be passed in (see above)
def within_limits(bag, n):
	return len(bag.contains) + n <= constraints.bag_max and len(bag.contains) + n >= constraints.bag_min

# checks if the given item is in any of the bags
#
# @param item - the item to check
# @param assignment - the current list of bags
# @return true if the item is in a bag, false otherwise
def isInAnyBag(item, assignment):
	for bag in assignment:
		if str(item) in str(bag.contains):
			return True

	return False

	
# Prunes cases in which adding the item to the specified bag
# will result in constraints not being satisfied
#
# @param item - item to add
# @param bag - bag to put item into
# @param assignment - current list of bags
# @return whether or not to prune this combination of bag and item
def arc_consistency(item, bag, assignment):
	# unary exclusive
	if item in list(constraints.un_excl.keys()):
		if bag.name in constraints.un_excl[item]:
			return False

	# unary inclusive
	if item in list(constraints.un_incl.keys()):
		if bag.name not in constraints.un_incl[item]:
			return False
			
	# mutually exclusive
	for key in list(constraints.bin_sim.keys()):
		if key[0] is item and bag.name in constraints.bin_sim[key]:
			if key[1] in bag.contains:
				return False
		elif key[1] is item and bag.name in constraints.bin_sim[key]:
			if key[0] in bag.contains:
				return False

	# binary not equals
	for pair in constraints.binarynotequals:
		if pair[0] is item and pair[1] in bag.contains:
			return False
		elif pair[1] is item and pair[0] in bag.contains:
			return False

	# binary equals
	for pair in constraints.binaryequals:
		if pair[0] is item:
			if pair[1] not in bag.contains and isInAnyBag(pair[1], assignment):
				return False
		elif pair[1] is item:
			if pair[0] not in bag.contains and isInAnyBag(pair[0], assignment):
				return False

	# fitting limits
	if constraints.bag_max is not 0:
		if len(bag.contains) + 1 > constraints.bag_max:
			return False

	return bag.wastedCapacity() >= items[item]


# Checks whether the constraint satisfaction problem is complete
#
# @param assignment - the current list of bags
# @return true if all constraints are satisfied, false otherwise
def isCSPcomplete(assignment):

	# check that all items are in a bag
	for item in items:
		if not isInAnyBag(item, assignment):
			return False

	# Fit limits and bag capacity check
	for bag in assignment:
		if bag.weight < math.floor(bag.capacity * 0.9) or bag.weight > bag.capacity:
			return False
		
		if constraints.bag_max != 0 and within_limits(bag, 0) == False:
			return False

	# Unary inclusive check
	for constraint in constraints.un_incl.items():
		variable = constraint[0]
		# find what bag that variable is in...
		target_bag = None
		for bag in assignment:
			if variable in bag.contains:
				target_bag = bag
				break
		if target_bag.name not in constraint[1]:
			return False
	
	#Unary exclusive check
	for constraint in constraints.un_excl.items():
		variable = constraint[0]
		# find what bag that variable is in...
		target_bag = None
		for bag in assignment:
			if variable in bag.contains:
				target_bag = bag
				break

		if target_bag in constraint[1]:
			return False


	#Binary constraints

	#Equal
	for constraint in constraints.binaryequals:
		variableOne = constraint[0]
		variableTwo = constraint[1]

		for bag in assignment:
			if variableOne in bag.contains:
				if variableTwo not in bag.contains:
					return False

	#Not equal
	for constraint in constraints.binarynotequals:
		variableOne = constraint[0]
		variableTwo = constraint[1]

		for bag in assignment:
			if variableOne in bag.contains:
				if variableTwo in bag.contains:
					return False


	#Binary simultaneous
	for constraint in constraints.bin_sim.items():
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

	# everything is satisfied...CSP is complete
	return True


# Gets the next, most constrained, variable (item)
# Feeds a list of current unassigned variables to 
# min_remaining_var. 
# 
# @param assignment - list of bags
# @return most constrained value according to our heuristic
def nextUnassignedVariables(assignment):
	#assignment: [] of bags
	variables = list(items.keys())

	for i in list(items.keys()):
		if isInAnyBag(i, assignment):
			variables.remove(i)
			if len(variables) == 0:
				return []

	return min_remaining_var(variables, assignment)


# Implementation of the backtrack algorithm to sort items into bags
# based on constraints
#
# @param assignment - current list of bags
# @return the list of bags with all the items sorted in, or None if no solution
def Backtrack(assignment):
	if len(nextUnassignedVariables(assignment)) == 0:
		return None

	# complete unary inclusive additions first if an item only has one possible bag (most constrained)
	uninc1 = []
	for u in constraints.un_incl.keys():
		if len(constraints.un_incl[u]) == 1:
			uninc1.append([u, constraints.un_incl[u]])

	for itembag in uninc1:
		bag = None
		for b in assignment:
			if b.name is itembag[1]:
				bag = b
				bag.addItem(itembag[0], items[itembag[0]])
				break

	# try most constrained item first
	var = nextUnassignedVariables(assignment)

	# try most constrained item in least constrained bag first, 
	#then if it doesn't work, try second least constrained bag, etc
	for val in least_constraining_vals(var, assignment):
			if arc_consistency(var, val, assignment):
				val.addItem(var, items[var])
				Backtrack(list(assignment))

				if isCSPcomplete(assignment) == True:
					return assignment
				else:
					val.removeItem(var, items[var])
					

# Gets the next, most constrained, variable (item)
# using three heuristics, 1. # of bags an item can fit into,
# 2. # of unary constraints, 3. weight of item
# 
# @param items - list of items
# @param assignment - list of bags
# @return most constrained value according to our heuristic
def min_remaining_var(items, assignment):
	bags_per_item = {}

	for i in items:
		bags_per_item[i] = 0
		for b in assignment:
			if arc_consistency(i, b, assignment):
				bags_per_item[i] += 1
	
	sortedDict = sorted(bags_per_item, key = lambda x: (bags_per_item.get, checkUnaryConstraints(x), checkWeight(x)))
	
	return sortedDict[0]
	
	
# Secondary heuristic for finding the most constrained item
# The more negative a value, the more constraints it has. 
# If 0, no unary constraints.
#
# @param item - the item to assign a heuristic val to
# @return heuristic value for this item
def checkUnaryConstraints(var):
	ret = 0

	for c in constraints.un_incl.keys():
		if str(var) is str(c):
			ret += -1

	for c in constraints.un_excl.keys():
		if str(var) is str(c):
			ret += -1
	
	return ret


# Tertiary heuristic for finding the most constrained item
# The more negative a value, the more constraints it has using
# its size as a constraint so more favor given to larger items.
#
# @param item - the item to assign a heuristic val to
# @return heuristic value for this item
def checkWeight(item):
	return items[item]*-1

	
# Finds the least constraining bag for items to fit into by sorting on
# 1. the number of different items that can fit into the bag and 2. the
# amount of space needed to be filled in a bag
#
# @param items - the list of items
# @param assignment - the list of bags
# @return the most constrained bag based on the heuristic 
def least_constraining_vals(items, assignment):
	items_per_bag = {}

	for b in assignment:
		items_per_bag[b] = 0
		for i in items:
			if arc_consistency(i, b, assignment):
				items_per_bag[b] += 1
	
	#Flip dictionary
	sortedDict = sorted(items_per_bag, key = lambda x: (items_per_bag.get, fitCapacityHeuristic(x)))

	return reversed(sortedDict)
	
	
# Heuristic used in least_constraining_vals to rank bags
# based on space they need to fill.
#
# @param bag - the bag to check for space needed to fill
# @return - the heuristic value of the bag based on capacity and fit limits
def fitCapacityHeuristic(bag):
	ret = 0
	
	cap = math.floor(bag.capacity * 0.9)
	if bag.weight < cap:
			ret += cap-bag.weight
		
	if constraints.bag_max != 0:
		if len(bag.contains) < constraints.bag_min:
			ret += constraints.bag_min - len(bag.contains)

	return ret


# Prints the output of backtrack in the specified format
#
# @param assignment - final state of the bags
def output(assignment):
	for x in range(0,len(assignment)):
		bag = assignment[x]
		print(bag.name, "", end="")
		for variable in bag.contains:
			print(variable, "", end="")
		print(" ")

		print("number of items: " + str(len(bag.contains)))
		print("total weight: " + str(bag.weight) + "/" + str(bag.capacity))
		print("wasted capacity: " + str(bag.wastedCapacity()))
		print("")

		
# check proper commandline usage
if len(sys.argv) != 2:
	print("Proper usage is python csp.py inputfile")
	exit()

	
items = {}
bags = []

constraints = Constraint()

parseInput(sys.argv[1])

final = Backtrack(bags)

if final is not None:
	output(final)
	sys.exit(0)
else:
	print("no solution found")
	sys.exit(1)
