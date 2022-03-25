from parsing.token import TokenType
from operators import *

def evaluate(operators, states, loop_size):
    computed_rows = []
    for op in operators:
        computed_rows.append(__solve_operator(op, computed_rows, states, loop_size))
    last_row = computed_rows[-1].boolean_array
    return all(b == True for b in last_row)
    
def __solve_operator(op, computed_rows, states, loop_size):
    match op.oper():
        case TokenType.ATOM: return solve_atom(op, states)
        case TokenType.NOT: return solve_not(op, computed_rows)
        case TokenType.AND: return solve_and(op, computed_rows)
        case TokenType.OR: return solve_or(op, computed_rows)
        case TokenType.IMPL: return solve_impl(op, computed_rows)
        case TokenType.U: return solve_U(op, computed_rows, loop_size)
        case TokenType.X: return solve_X(op, computed_rows, loop_size)
        case TokenType.F: return solve_F(op, computed_rows, loop_size)
        case TokenType.R: return solve_R(op, computed_rows, loop_size)
        case TokenType.G: return solve_G(op, computed_rows, loop_size)
        case TokenType.W: return solve_W(op, computed_rows, loop_size)
        case _: raise Exception("No available implementation for operator " + op)       
