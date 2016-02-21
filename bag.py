# Project 5 - CSP
# Theresa Inzerillo & Preston Mueller
# CS4341 Introduction to Artificial Intelligence
#
# Bag object class

class Bag:
	def __init__(self, name, capacity):
		self._name = name
		self._capacity = capacity
		self._weight = 0
		self._contains = [] 

	@property
	def name(self):
		return self._name
		
	@property
	def capacity(self):
		return self._capacity
		
	@property
	def weight(self):
		return self._weight
			
	@property
	def contains(self):
		return self._contains

	def wastedCapacity(self):
		return self.capacity-self.weight

	def addItem(self, type, number):
		if type not in self._contains:
			self._contains.append(type)
		self._weight += number
		
	def removeItem(self, type, number):
		if type in self.contains:
			self.contains.remove(type)
		self._weight -= number