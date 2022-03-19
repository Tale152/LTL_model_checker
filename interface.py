from parsing.parser import Parser 
from parsing.lexer import Lexer 
from input_paths.path import Path, State

# To use the parsed formula's AST, you will need
# to import class Ast from ast. Ast comes equipped 
# with the following useful functions:
# arity(), which returns the arity of the topmost 
# operator in the syntax tree;
# oper(), which returns the type of that operator
# --- operators are of class Token and their type
# is one of the types in TokenType (see token.py);
# children() returns a list of the children of the
# formula (with the left child first) --- for 
# example, if t is the AST of formula A U B, then
# t.children() is the list [l,r], where l is the 
# AST of A and r the AST of B;
# for convenience, when the topmost operator's 
# arity is 1, child() returns the AST's only child
# (not as a list).
# The ASTs returned by the parser are equipped with
# equality, so for two AST t, s given by the parser, 
# we have t == s when they represent the same formula.



def parse(string):
# Parses a string and returns an abstract 
# syntax tree (AST) of the formula written 
# in the string, as long as the formula is 
# written in an appropriate format. Allowed 
# symbols:
# words from letters, numbers, and _ for 
#    propositional variables;
# ! && || -> for propositional connectives;
# X G F U W R for LTL operators.
	return Parser(Lexer(string)).parse()


def getpath(string):
# Returns a Path object that encodes a path in a 
# transition system. Attribute length is the number 
# of states in the path; attribute loop is the
# number of states that are repeated in a loop at 
# the end of the path; attribute path is a list of
# the states in the path in order, as State objects
# (see the documentation of the State class for that. 
# Method all_propositions() returns a list of all 
# propositions that appear in the path (without 
# duplicates), and next_state() lets you traverse 
# the infinite path, starting from the first state.
	return Path(string)