""" Represents an abstract syntax tree node for a generic parser. """
class Ast(object):
  
  def __str__(self):
    """ Returns the readable string representation of the token instance."""
    if isinstance(self, Atom):
      return Ast._indent(str(self.value))
    elif isinstance(self, Unary):
      return Ast._indent(str(self.value) + ' {\n' + str(self.right) + '\n}')
    elif isinstance(self, Binary):
      return Ast._indent(str(self.value) + ' {\n' + str(self.left) + ',\n' + str(self.right) + '\n}')

  def __repr__(self):
    """ Returns the unambiguous string representation of the token instance.""" 
    return self.__str__()

  def __eq__(self, other):
    """ Returns True if the other object is equal to this one, otherwise False 
        is returned. 
    """
    return (
      self.__class__ == other.__class__ and
      self.value == other.value
    )

  def arity(self):
    if isinstance(self, Atom):
      return 0
    elif isinstance(self, Unary):
      return 1
    elif isinstance(self, Binary):
      return 2

  def as_dot(self):    
    """ Returns the representation of this node in .dot format which can be
        viewed with a .dot compatible plotter such as GraphViz or GraphViz 
        online (https://dreampuf.github.io/GraphvizOnline/).
    """
    node_labels = ''
    for (id, node) in self._node_list(0):
      node_labels += '{0}[label="{1}"];\n'.format(id, node)

    (_, tree) = self._as_dot(0)

    return 'graph ast {{\n{0}\n{1}\n}}'.format(node_labels, tree)

  @staticmethod
  def _indent(text):
    """ Indents the specified text. """
    indented, lines = '', text.splitlines(True)
    for line in lines:
      indented += '..' + line
    return indented

  def _node_list(self, id):
    if isinstance(self, Atom):
      return [(id + 1, self.value)]
    elif isinstance(self, Unary):
      r_nodes = self.right._node_list(id)
      (r_id, _) = r_nodes[-1]
      return r_nodes + [(r_id + 1, self.value)]
    elif isinstance(self, Binary):
      l_nodes = self.left._node_list(id)
      (l_id, _) = l_nodes[-1]
      r_nodes = self.right._node_list(l_id)
      (r_id, _) = r_nodes[-1]
      return l_nodes + r_nodes + [(r_id + 1, self.value)]

  def _as_dot(self, id):
    if isinstance(self, Atom):
      return (id + 1, '{0}'.format(id + 1))
    elif isinstance(self, Unary):
      (r_id, r_nodes) = self.right._as_dot(id)
      return (r_id + 1, '{0}--{1}'.format(r_id + 1, r_nodes))
    elif isinstance(self, Binary):
      (l_id, l_nodes) = self.left._as_dot(id)
      (r_id, r_nodes) = self.right._as_dot(l_id)
      return (r_id + 1, '{0}--{1};\n{0}--{2}'.format(r_id + 1, l_nodes, r_nodes))
  
  def oper(self):
    return self.value.type

  # def operstring(self):
  #   self.value.value

  def children(self):
    if self.arity() == 0:
      return []
    elif self.arity() == 1:
      return [self.right]
    elif self.arity() == 2:
      return [self.left,self.right]

  def child(self):
    if self.arity() == 1:
      return self.right
    else:
      return None


    
""" Represents an abstract syntax tree node for an atomic propositional 
    variable. 
"""
class Atom(Ast):

  def __init__(self, value):
    """ Initializes the propositional variable abstract syntax tree node with 
        the specified token value. 
    """
    self.value = value

""" Represents an abstract syntax tree node for a unary operator. """
class Unary(Ast):

  def __init__(self, value, right):
    """ Initializes the propositional variable abstract syntax tree node with 
        the specified token value and right sub-tree. 
    """
    self.value = value
    self.right = right

  def __eq__(self, other):
    """ Returns True if the other object is equal to this one, otherwise False 
        is returned. 
    """
    return (
      super().__eq__(other) and 
      self.right == other.right
    )

""" Represents and abstract syntax tree node for a binary operator. """
class Binary(Ast):

  def __init__(self, value, left, right):
    """ Initializes the propositional variable abstract syntax tree node with 
        the specified token value and left and right sub-trees.
    """
    self.value = value
    self.left = left
    self.right = right

  def __eq__(self, other):
    """ Returns True if the other object is equal to this one, otherwise False 
        is returned. 
    """
    return (
      super().__eq__(other) and 
      self.right == other.right and self.left == other.left
    )

