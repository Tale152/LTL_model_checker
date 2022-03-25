from Row import Row
from parsing.token import TokenType
from operators import solve_atom, solve_not, solve_and, solve_or, solve_impl, solve_U, solve_X, solve_F, solve_R, solve_G

def solve_operator(op, computed_rows, states, loop_size):
    token = op.oper()
    if token == TokenType.ATOM:
        return solve_atom(op, states)
    elif token == TokenType.NOT:
        return solve_not(op, computed_rows)
    elif token == TokenType.AND:
        return solve_and(op, computed_rows)
    elif token == TokenType.OR:
        return solve_or(op, computed_rows)
    elif token == TokenType.IMPL:
        return solve_impl(op, computed_rows)
    elif token == TokenType.U:
        return solve_U(op, computed_rows, loop_size)
    elif token == TokenType.X:
        return solve_X(op, computed_rows, loop_size)
    elif token == TokenType.F:
        return solve_F(op, computed_rows, loop_size)
    elif token == TokenType.R:
        return solve_R(op, computed_rows, loop_size)
    elif token == TokenType.G:
        return solve_G(op, computed_rows, loop_size)
    else:
        raise Exception("No available implementation for token " + token)

def define_result(last_boolean_row):
    for r in last_boolean_row:
        if r == False:
            return False
    return True

def evaluate(operators, states, loop_size):
    computed_rows = []
    for op in operators:
        computed_rows.append(solve_operator(op, computed_rows, states, loop_size))
    return define_result(computed_rows[-1].boolean_array)
