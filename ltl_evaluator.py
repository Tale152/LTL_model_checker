from Row import Row
from parsing.token import TokenType
from operators import solve_atom, solve_not

def solve_operator(op, computed_rows, states):
    token = op.oper()
    if token == TokenType.ATOM:
        return solve_atom(op, states)
    if token == TokenType.NOT:
        return solve_not(op, computed_rows)
    else:
        #TODO
        Row(op, [])

def define_result(last_boolean_row):
    for r in last_boolean_row:
        if r == False:
            return False
    return True

def evaluate(operators, states):
    computed_rows = []
    for op in operators:
        computed_rows.append(solve_operator(op, computed_rows, states))
    return define_result(computed_rows[-1].boolean_array)
