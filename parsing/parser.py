from parsing.token import Token, TokenType
from parsing.ast import Binary, Unary, Atom

# The BNF for the LTL grammar. Still need to check it!
# <formula> ::= <or-expr> '->' <formula> | <or-expr>; Right associative
## <or-expr> ::= <and-expr> '||' <or-expr> | <and-expr>; 
## <and-expr> ::= <binary-expr> '&&' <and-expr> | <binary-expr>; 
# <or-expr> ::= <and-expr> '||' <and-expr> | <or-expr>; Left associative
# <and-expr> ::= <binary-expr> '&&' <binary-expr> | <and-expr>; Left associative
# <binary-expr> ::= <unary-expr> 'U' <binary-expr> | <unary-expr>; Right associative
# <unary-expr> ::= ['X']<unary-expr> | <prop>; Right associative
# <prop> ::= <atom> | '(' <formula> ')' | <formula>); 
# <atom> ::= <letter> | ‘_’ (<letter> | <digit> | ‘_’ ) <atom>;
# <letter> ::= ‘A’ | ‘B’ | .. | ‘Z’ | ‘a’ | ‘b’ | .. | ‘z’;
# <digit> ::= ‘0’ | ‘1’ | .. | ‘9’;
# <or-op> ::= '||' | '->'
# <and-op> ::= '&&'
# <neg-op> ::= '!'
# <gfx-op> ::= 'G' | 'F' | 'X'
# <uwr-op> ::= 'U' | 'W' | 'R'

""" A parser for the LTL grammar. 
    
    The class is initialized with the lexical analyser which has not yet been
    used. A full abstract syntax tree of the parsed syntax can be obtained by
    invoking the parse() method. Errors are raised by this method if invalid
    syntax is encountered by the parser. The error details both the line and 
    column of where the parse error occurred, while the error message also 
    includes the exact position in the input string where the error occurred.
"""
class Parser(object):

  def __init__(self, lexer):
    """ Initializes the parser with an unused lexer. """
    self._lexer = lexer
    self._look_ahead = lexer.get_next_token()

  def _error(self, message, line, col):
    hint = self._lexer.text[:col - 1] + '^^^' + self._lexer.text[col - 1:]
    raise Exception('Parse error (%s,%s): %s. Hint: %s.' % (line, col, message, hint))

  def _read_next_token(self):
    """ Reads the next token from the lexer. """
    self._look_ahead = self._lexer.get_next_token()

  def parse(self):
    """ Parses the tokens in the lexer and returns the full abstract syntax 
        tree. 
    """
    return self._parse_formula(0)

  def _parse_formula(self, level):
    """ Parses the top-level formula consisting of the 'implies' operator -> 
        and its left and right sub-branches or only the 'or' expression branch. 
        Parsing is performed in a right-associative fashion by consuming -> 
        operators using right-recursive productions.
    """
    node = self._parse_or_expr(level)
    token = self._look_ahead

    if token.type == TokenType.IMPL:
      self._read_next_token()
      right = self._parse_formula(level)
      node = Binary(token, node, right)
    elif token.type == TokenType.RPAR and level == 0:
      self._error('extra )', token.line, token.col)
    elif token.type != TokenType.EOF and level == 0:
      self._error('unexpected operator ' + token.value, token.line, token.col)
    
    return node
  
  # Say thar right associatve are handled with a loop
  def _parse_or_expr(self, level):
    """ Parses the 'or' expression consisting of the 'or' operator || and its 
        left and right sub-branches or only the 'and' expression branch.
        Parsing is performed in a left-associative fashion by consuming || 
        operators in a loop.
    """
    node = self._parse_and_expr(level)

    while self._look_ahead.type == TokenType.OR:
      token = self._look_ahead
      self._read_next_token()
      node = Binary(token, node, self._parse_and_expr(level))

    return node

  def _parse_and_expr(self, level):
    """ Parses the 'and' expression consisting of the 'and' operator && and its
        left and right sub-branches or only the 'binary' expression branch.
        Parsing is performed in a left-associative fashion by consuming &&
        operators in a loop.
    """
    node = self._parse_binary_expr(level)

    while self._look_ahead.type == TokenType.AND:
      token = self._look_ahead
      self._read_next_token()
      node = Binary(token, node, self._parse_binary_expr(level))      

    return node

  def _parse_binary_expr(self, level):
    """ Parses the binary temporal expression consisting of one of the temporal
        operators U, R or W and its left and right sub-branches or only the 
        unary expression branch.
        Parsing is performed in a right-associative fashion by consuming the 
        binary temporal operator using right-recursive productions.
    """
    node = self._parse_unary_expr(level)
    token = self._look_ahead

    if token.type in (TokenType.U, TokenType.W, TokenType.R):
      self._read_next_token()
      right = self._parse_binary_expr(level)
      node = Binary(token, node, right)

    return node

  def _parse_unary_expr(self, level):
    """ Parses the unary temporal/logical expression consisting of one of the
        temporal operators G, F or X or the logical operator !, and its left
        and right sub-branches. 
        Parsing is performed in a right-associative fashion by consuming the
        unary operator using right-recursive productions.
    """
    token = self._look_ahead  

    if token.type in (TokenType.NOT, TokenType.G, TokenType.F, TokenType.X):
      self._read_next_token()
      right = self._parse_unary_expr(level)
      return Unary(token, right)

    return self._parse_prop_expr(level)

  def _parse_prop_expr(self, level):
    """ Parses the formula expression that leads either to the non-recursive 
        expression ending in a propositional variable (called atom here) or 
        the recursive bracketed expression.
        Errors are raised in case the bracketed expression is incorrectly 
        balanced or if the sub-formula is missing.
    """
    token = self._look_ahead      
  
    if self._look_ahead.type == TokenType.ATOM:
      node = self._parse_atom_expr()
    elif self._look_ahead.type == TokenType.LPAR:
      self._read_next_token()
      node = self._parse_formula(level + 1)

      # Check for missing left bracket
      if self._look_ahead.type != TokenType.RPAR:
        self._error('missing )', self._look_ahead.line, self._look_ahead.col)
      self._read_next_token()
    else:
      self._error('expected sub-formula or proposition', self._look_ahead.line, self._look_ahead.col)

    return node

  def _parse_atom_expr(self):
    """ Parses the propositional variable (called atom here). """
    token = self._look_ahead
    self._read_next_token()
    return Atom(token)    













