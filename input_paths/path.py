from parsing.parser import Parser
from parsing.ast import Binary, Unary, Atom
from parsing.token import Token
from parsing.lexer import Lexer

# extracting paths from files
#

class Path(object):
	def __init__(self,filename):
		all_lines = open(filename).readlines()
		nums = all_lines[0].split()
		self.total, self.loop = int(nums[0]), int(nums[1])
		self.path = self.get_path(all_lines[1:]) 
		if len(self.path) != self.total:
			print ("wrong path input: the parameters do not match")

	def all_propositions(self):
	# Returns a list of all propositional variables that appear in
	# the path. It removes duplicates.
		everything = [prp for stt in self.path for prp in stt.labeling ]
		less = []
		for x in everything:
			if not x in less:
				less.append(x)
		return less


	def next_state(self):
	# Starting from the first state of the path, it transitions
	# through the states in sequence (going through the end loop
	# infinitely many times).
		i = 0
		initial = total - loop
		while True:
			if i >= total:
				i -= loop
			yield self.path[i]


	def get_prop(self,str):
		in_prop = False
		prop = ''
		empty = True
		for pos,x in enumerate(str):
			if x.isalpha():
				in_prop = True
			if in_prop and x.isspace():
				return Parser(Lexer(prop)).parse(), pos
			if in_prop:
				prop += x
		if in_prop:
			prop.strip('\n')
			return Parser(Lexer(prop)).parse(), len(str)
		return None, 0


	def get_state(self,ident,str):
		state = []
		position = 0
		while position < len(str):
			temp_state, temp_position = self.get_prop(str[position:])
			if temp_state != None:
				state += [temp_state]
			position += temp_position + 1
		# print(state)
		return State(ident,state) 


	def get_path(self,list):
		return [self.get_state(i,s) for i,s in enumerate(list)]


class State(object):
# A state has a unique (for each path) identifier and a set of
# propositions that represents its labeling. That is propositional
# variable p holds in state s iff p is in s.labeling
	def __init__(self, ident, list = 0):
		self.ident = ident
		self.labeling = list
		