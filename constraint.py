# Project 5 - CSP
# Theresa Inzerillo & Preston Mueller
# CS4341 Introduction to Artificial Intelligence
#
# Constraint object class

class Constraint():

	def __init__(self):
		self.bag_min = 0
		self.bag_max = 0
		self.binaryequals = []
		self.binarynotequals = []
		self.un_incl = {}
		self.un_excl = {}
		self.bin_sim = {}