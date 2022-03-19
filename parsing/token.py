from enum import Enum

""" Denotes the different kinds of token types that can appear in the source 
    text.
"""
TokenType = Enum('TokenType', [
  'EOF', 'NIL', # Control tokens.
  'AND', 'OR', 'NOT', 'IMPL', 'ATOM', # Propositional logic tokens.
  'G', 'X', 'F', 'U', 'W', 'R', # Linear temporal logic tokens.
  'LPAR', 'RPAR' # Meta precedence symbol tokens.
  ])

""" Represents a generic token. """
class Token(object):

  def __init__(self, type = TokenType.NIL, value = '<NIL>', line = 0, col = 0):
    """ Initializes the token with the specified token type and textual value.
        The line and column number indicate the location of the token in the 
        source text, and default both to 0.
    """
    self.type = type
    self.value = value
    self.line = line
    self.col = col

  def __str__(self):
    """ Returns the readable string representation of the token instance."""
    # return 'Token({type}, {value} @ {line}:{col})'.format(
    #   type = self.type, 
    #   value = repr(self.value), 
    #   line = self.line, 
    #   col = self.col)
    return self.value

  def __repr__(self):
    """ Returns the unambiguous string representation of the token instance.""" 
    return self.__str__()

  def __eq__(self, other):
    """ Returns True if the other object is equal to this one, otherwise False 
        is returned. 
    """
    return (
      self.__class__ == other.__class__ and
      self.type == other.type and self.value == other.value
    )

  def is_whitespace(char):
    """ Determines whether the specified character is a white space. """
    return char is not None and char.isspace()

  def is_alpha(char):
    """ Determines whether the specified character is an alphanumeric. """
    return char is not None and (char.isalpha() or char.isdigit() or char == '_')

  def is_digit(char):
    """ Determines whether the specified character is a digit. """
    return char is not None and char.isdigit()

  def is_operator(char):
    """ Determines whether the specified character is a multi-character operator
        symbol. 
    """
    return char in ('&', '|', '-', '>')

  def is_symbol(char):
    """ Determines whether the specified character is a single-character 
        symbol. 
    """
    return char in ('!', '(', ')')