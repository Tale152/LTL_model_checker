from parsing.token import Token, TokenType

""" A lexical analyser for LTL.
    
    The class is initialized with a string containing the LTL formula, and 
    tokens can then be retrieved from the string in a lazy fashion by invoking 
    the get_next_token() method. Only significant tokens are returned by the
    method, meaning that white-space characters are gobbled up and ignored.
    As the lexical analyses takes place lazily, errors are only raised when the
    analysis encounters illegal characters in the string.
"""
class Lexer(object):

  def __init__(self, text):
    """ Initializes the lexical analyser with the input formula to tokenize, 
        together with the counters. The look-ahead character is also 
        bootstrapped by immediately reading the first character from the stream. 
    """
    self.text = text
    self._pos, self._col, self._line = -1, 0, 1

    # Initialize look-ahead to the first character in the input stream.
    self._look_ahead = ''
    self._read_next_char()
    
  def _error(self, message, line, col):
    hint = self.text[:col - 1] + '^^^' + self.text[col - 1:]
    raise Exception('Lexical error (%s,%s): %s. Hint: %s.' % (line, col, message, hint))

  def _read_next_char(self):
    """ Reads the next character from the string and updates the look ahead 
        character or sets it to None if the string is depleted.
    """
    self._pos, self._col = self._pos + 1, self._col + 1

    if self._pos > len(self.text) - 1:
      # We have reached the end of the input string.
      self._look_ahead = None
    else:
      # Get next character from the input string.
      self._look_ahead = self.text[self._pos]

  def _skip_whitespace(self):
    """ Eats up all the white space character by character until a non-white 
        space character is encountered in the input stream.
    """
    while self._look_ahead is not None and self._look_ahead.isspace():
      if self._look_ahead == '\n' or self._look_ahead == '\r\n':
        self._line, self._col = self._line + 1, 0
      self._read_next_char()

  def get_next_token(self):
    """ Returns the next token from the string. """
    if Token.is_whitespace(self._look_ahead):
      self._skip_whitespace()

    if self._look_ahead is None:
      return Token(TokenType.EOF, '<EOF>', self._line, self._col)
    elif Token.is_alpha(self._look_ahead):
      return self._get_word()
    elif Token.is_operator(self._look_ahead):
      return self._get_operator()
    elif Token.is_symbol(self._look_ahead):
      return self._get_symbol()

    return self._error('invalid character: \'' + self._look_ahead + '\'', self._line, self._col)

  def _get_word(self):
    """ Returns the next word string from the input stream as a token. """
    word, line, col = '', self._line, self._col
    while Token.is_alpha(self._look_ahead):
      word += self._look_ahead
      self._read_next_char()
    return Token(Lexer._token_type_from_word(word), word, line, col)

  def _get_operator(self):
    """ Returns the next operator from the input stream as a token. """
    operator, line, col = '', self._line, self._col
    while Token.is_operator(self._look_ahead):
      operator += self._look_ahead
      self._read_next_char()
    return Token(Lexer._token_type_from_operator(operator), operator, line, col)

  def _get_symbol(self):
    """ Returns the next symbol from the input stream as a token. """
    symbol, line, col = self._look_ahead, self._line, self._col
    self._read_next_char()
    return Token(Lexer._token_type_from_symbol(symbol), symbol, line, col)
     
  def _token_type_from_word(value):
    """ Returns the temporal operator or proposition token type from the 
        specified word value. 
    """
    return {
        'G': TokenType.G,
        'X': TokenType.X,
        'F': TokenType.F,
        'U': TokenType.U,
        'W': TokenType.W,
        'R': TokenType.R        
    }.get(value, TokenType.ATOM)

  def _token_type_from_operator(value):
    """ Returns the multi-character token type from the specified symbol 
        value. """
    return {
        '&&': TokenType.AND,
        '||': TokenType.OR,
        '->': TokenType.IMPL
    }.get(value)

  def _token_type_from_symbol(value):
    """ Returns the single-character token type from the specified symbol 
        value. """
    return {
        '!': TokenType.NOT,
        '(': TokenType.LPAR,
        ')': TokenType.RPAR
    }.get(value)