from parsing.token import TokenType
from operators import OperatorsSolver

def evaluate(operators, states, loop_size):
    computed_rows = []
    solver = OperatorsSolver(states, loop_size, computed_rows)
    for op in operators:
        computed_rows.append(__solve_operator(op, solver))
    last_row = computed_rows[-1].boolean_array
    return all(b == True for b in last_row)
    
def __solve_operator(op, solver):
    match op.oper():
        case TokenType.ATOM: return solver.solve_atom(op)
        case TokenType.NOT: return solver.solve_not(op)
        case TokenType.AND: return solver.solve_and(op)
        case TokenType.OR: return solver.solve_or(op)
        case TokenType.IMPL: return solver.solve_impl(op)
        case TokenType.U: return solver.solve_U(op)
        case TokenType.X: return solver.solve_X(op)
        case TokenType.F: return solver.solve_F(op)
        case TokenType.R: return solver.solve_R(op)
        case TokenType.G: return solver.solve_G(op)
        case TokenType.W: return solver.solve_W(op)
        case _: raise Exception("No available implementation for operator " + op)       
