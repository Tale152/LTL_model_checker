from Row import Row
from base_operators import create_array_with_value, U_operator, X_operator, OR_operator, NOT_operator

# ---- utility functions ----
def find_row(op, computed_rows):
    for r in computed_rows:
        if r.operator == op:
            return r
    raise Exception("operator from previously computed rows not found: " + str(op.value))

def get_left_child(op, computed_rows):
    return find_row(op.children()[0], computed_rows).boolean_array

def get_right_child(op, computed_rows):
    return find_row(op.children()[1], computed_rows).boolean_array

# ---- 0 arity operators ----

def solve_atom(op, states):
    prop = ".." + str(op.value)
    bool_row = []
    for s in states:
        found = False
        for l in s.labeling:
            if str(l) == prop:
                found = True
        bool_row.append(found)
    return Row(op, bool_row)
    
# ---- 1 arity operators ----

def solve_X(op, computed_rows, loop_size):
    child = get_left_child(op, computed_rows)
    # base operator
    return Row(op, X_operator(child, loop_size))

def solve_not(op, computed_rows):
    child = get_left_child(op, computed_rows)
    # base operator
    return Row(op, NOT_operator(child))

# ---- 2 arity operators ----

def solve_U(op, computed_rows, loop_size):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    # base operator
    return Row(op, U_operator(left_child, right_child, loop_size))

def solve_or(op, computed_rows):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    # base operator
    return Row(op, OR_operator(left_child, right_child))

def solve_impl(op, computed_rows):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    # a -> b == !a || b
    return Row(op, OR_operator(NOT_operator(left_child), right_child))

def solve_and(op, computed_rows):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    # a && b == !(!a || !b)
    return Row(op, NOT_operator(OR_operator(NOT_operator(left_child), NOT_operator(right_child))))

def solve_F(op, computed_rows, loop_size):
    child = get_left_child(op, computed_rows)
    true_arr = create_array_with_value(len(child), True)
    # F(a) == true U a
    return Row(op, U_operator(true_arr, child, loop_size))

def solve_R(op, computed_rows, loop_size):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    # a R b == !(!a U !b)
    U = U_operator(NOT_operator(left_child), NOT_operator(right_child), loop_size)
    return Row(op, NOT_operator(U))

def solve_G(op, computed_rows, loop_size):
    child = get_left_child(op, computed_rows)
    true_arr = create_array_with_value(len(child), True)
    # G(a) == false R a == !F(!a) == !(true U !a)
    U = U_operator(true_arr, NOT_operator(child), loop_size)
    return Row(op, NOT_operator(U))

def solve_W(op, computed_rows, loop_size):
    a = get_left_child(op, computed_rows)
    b = get_right_child(op, computed_rows)
    # a W b == (a U b) || G(a) == a U (b || G(a)) == b R (b || a) == !(!b U !(b || a))
    OR = OR_operator(b, a)
    U = U_operator(NOT_operator(b), NOT_operator(OR), loop_size)
    return Row(op, NOT_operator(U))
