# Project 5 - CSP
# Theresa Inzerillo & Preston Mueller
# CS4341 Introduction to Artificial Intelligence

class Bag:

	def __init__(self, name, capacity):
		self.name = name
		self.capacity = capacity
		self.count = 0
		self.contains = []

	@property
	def name(self):
		return self._name
		
	@property
	def capacity(self):
		return self._capacity
		
	@property
	def count(self):
		return self._count
			
	@property
	def contains(self):
		return self._contains

	def weight(self):
		pass

	def wastedCapacity(self):
		return self.capacity-self.count

	def addItem(self, type, number):
		if type not in self.contains:
			self.contains.append(type)
		self.count += number
		
	def removeItem(self, type, number):
		if type in self.contains:
			self.contains.remove(type)
		self.count -= number