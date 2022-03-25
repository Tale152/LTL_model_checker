from Row import Row
from base_operators import *
from util import *

class OperatorsSolver:

    def __init__(self, states, loop_size, computed_rows):
        self.states = states
        self.loop_size = loop_size
        self.computed_rows = computed_rows

    # ---- 0 arity operators ----

    def solve_atom(self, op):
        bool_row = []
        for s in self.states:
            bool_row.append(op in s.labeling)
        return Row(op, bool_row)
        
    # ---- 1 arity operators ----

    def solve_not(self, op):
        child = get_child_boolean_array(op, self.computed_rows)
        # base operator
        return Row(op, NOT_operator(child))

    def solve_X(self, op):
        child = get_child_boolean_array(op, self.computed_rows)
        # base operator
        return Row(op, X_operator(child, self.loop_size))

    def solve_F(self, op):
        child = get_child_boolean_array(op, self.computed_rows)
        true_arr = create_array_with_value(len(child), True)
        # F(a) == true U a
        return Row(op, U_operator(true_arr, child, self.loop_size))

    def solve_G(self, op):
        child = get_child_boolean_array(op, self.computed_rows)
        true_arr = create_array_with_value(len(child), True)
        # G(a) == false R a == !F(!a) == !(true U !a)
        U = U_operator(true_arr, NOT_operator(child), self.loop_size)
        return Row(op, NOT_operator(U))

    # ---- 2 arity operators ----

    def solve_U(self, op):
        a = get_left_child_boolean_array(op, self.computed_rows)
        b = get_right_child_boolean_array(op, self.computed_rows)
        # base operator
        return Row(op, U_operator(a, b, self.loop_size))

    def solve_or(self, op):
        a = get_left_child_boolean_array(op, self.computed_rows)
        b = get_right_child_boolean_array(op, self.computed_rows)
        # base operator
        return Row(op, OR_operator(a, b))

    def solve_impl(self, op):
        a = get_left_child_boolean_array(op, self.computed_rows)
        b = get_right_child_boolean_array(op, self.computed_rows)
        # a -> b == !a || b
        return Row(op, OR_operator(NOT_operator(a), b))

    def solve_and(self, op):
        a = get_left_child_boolean_array(op, self.computed_rows)
        b = get_right_child_boolean_array(op, self.computed_rows)
        # a && b == !(!a || !b)
        return Row(op, NOT_operator(OR_operator(NOT_operator(a), NOT_operator(b))))

    def solve_R(self, op):
        a = get_left_child_boolean_array(op, self.computed_rows)
        b = get_right_child_boolean_array(op, self.computed_rows)
        # a R b == !(!a U !b)
        U = U_operator(NOT_operator(a), NOT_operator(b), self.loop_size)
        return Row(op, NOT_operator(U))

    def solve_W(self, op):
        a = get_left_child_boolean_array(op, self.computed_rows)
        b = get_right_child_boolean_array(op, self.computed_rows)
        # a W b == (a U b) || G(a) == a U (b || G(a)) == b R (b || a) == !(!b U !(b || a))
        OR = OR_operator(b, a)
        U = U_operator(NOT_operator(b), NOT_operator(OR), self.loop_size)
        return Row(op, NOT_operator(U))
