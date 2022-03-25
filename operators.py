from Row import Row
from base_operators import U_operator, X_operator, OR_operator, NOT_operator

def find_row(op, computed_rows):
    for r in computed_rows:
        if r.operator == op:
            return r
    raise Exception("operator from previously computed rows not found: " + str(op.value))

def get_left_child(op, computed_rows):
    return find_row(op.children()[0], computed_rows).boolean_array

def get_right_child(op, computed_rows):
    return find_row(op.children()[1], computed_rows).boolean_array
    
def solve_X(op, computed_rows, loop_size):
    child = get_left_child(op, computed_rows)
    return Row(op, X_operator(child, loop_size))

def solve_U(op, computed_rows, loop_size):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    return Row(op, U_operator(left_child, right_child, loop_size))

def solve_impl(op, computed_rows):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    return Row(op, OR_operator(NOT_operator(left_child), right_child))

def solve_or(op, computed_rows):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    return Row(op, OR_operator(left_child, right_child))

def solve_and(op, computed_rows):
    left_child = get_left_child(op, computed_rows)
    right_child = get_right_child(op, computed_rows)
    return Row(op, NOT_operator(OR_operator(NOT_operator(left_child), NOT_operator(right_child))))

def solve_not(op, computed_rows):
    child = get_left_child(op, computed_rows)
    return Row(op, NOT_operator(child))

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