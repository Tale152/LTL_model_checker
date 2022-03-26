from Row import Row
from base_operators import BaseOperatorsSolver
from util import *

class OperatorsSolver:

    def __init__(self, states, loop_size, computed_rows):
        self.states = states
        self.bo = BaseOperatorsSolver(loop_size)
        self.computed_rows = computed_rows

    def ATOM(self, op):
        bool_row = []
        for s in self.states:
            bool_row.append(op in s.labeling)
        return Row(op, bool_row)
        
    # ---- unary operators ----

    def __solve_unary_operator(self, op, strategy):
        child = get_child_boolean_array(op, self.computed_rows)
        return Row(op, strategy(child))

    def NOT(self, op):
        return self.__solve_unary_operator(op, self.bo.NOT)

    def X(self, op):
        return self.__solve_unary_operator(op, self.bo.X)

    def F(self, op): # F(a) == true U a
        F_strategy = lambda a: self.bo.U(true_array(len(a)), a)
        return self.__solve_unary_operator(op, F_strategy)

    def G(self, op): # G(a) == false R a == !F(!a) == !(true U !a)
        G_strategy = lambda a: self.bo.NOT(self.bo.U(true_array(len(a)), self.bo.NOT(a)))
        return self.__solve_unary_operator(op, G_strategy)

    # ---- binary operators ----

    def __solve_binary_operator(self, op, strategy):
        a = get_left_child_boolean_array(op, self.computed_rows)
        b = get_right_child_boolean_array(op, self.computed_rows)
        return Row(op, strategy(a, b))

    def U(self, op):
        return self.__solve_binary_operator(op, self.bo.U)

    def OR(self, op):
        return self.__solve_binary_operator(op, self.bo.OR)

    def IMPL(self, op): # a -> b == !a || b
        IMPL_strategy = lambda a, b: self.bo.OR(self.bo.NOT(a), b)
        return self.__solve_binary_operator(op, IMPL_strategy)

    def AND(self, op): # a && b == !(!a || !b)
        AND_strategy = lambda a, b: self.bo.NOT(self.bo.OR(self.bo.NOT(a), self.bo.NOT(b)))
        return self.__solve_binary_operator(op, AND_strategy)

    def R(self, op): # a R b == !(!a U !b)
        R_strategy = lambda a, b: self.bo.NOT(self.bo.U(self.bo.NOT(a), self.bo.NOT(b)))
        return self.__solve_binary_operator(op, R_strategy)

    def W(self, op): # a W b == (a U b) || G(a) == a U (b || G(a)) == b R (b || a) == !(!b U !(b || a))
        W_strategy = lambda a, b: self.bo.NOT(self.bo.U(self.bo.NOT(b), self.bo.NOT(self.bo.OR(b, a))))
        return self.__solve_binary_operator(op, W_strategy)
