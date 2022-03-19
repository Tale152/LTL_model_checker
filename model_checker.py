from interface import parse, getpath
from parsing.parser import Parser
from parsing.lexer import Lexer
from input_paths.path import Path 
from parsing.ast import Ast
from parsing.token import Token, TokenType


# A model checker for LTL on regular paths


def evaluate(path,form):
	# You do not have to use evaluate as it is here;
	# you can implement modelcheck however you like.
	# This is only a hint.
	pass
	


def modelcheck(m,f):
	return evaluate(m,f)[0]
