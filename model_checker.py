from interface import parse, getpath
from parsing.token import TokenType

from model_checking.operators import OperatorsSolver
from model_checking.ordered_operators_extractor import extract_ordered_operators_array
from model_checking.ordered_operators_extractor import extract_ordered_operators_array

# A model checker for LTL on regular paths

# m: String defining the path on filesystem to the model
# f: String defining the LTL formula to check
# returns True if the model satisfies the LTL formula, False otherwise
def modelcheck(m,f):
	path_object = getpath(m)
	parsed_formula = parse(f)
	return evaluate(extract_ordered_operators_array(parsed_formula), path_object.path, path_object.loop)

def evaluate(operators, states, loop_size):
    computed_rows = []
    solver = OperatorsSolver(states, loop_size, computed_rows)
    for op in operators:
        computed_rows.append(__solve_operator(op, solver))
    last_row = computed_rows[-1].boolean_array
    return all(b == True for b in last_row)
    
def __solve_operator(op, solver):
    match op.oper():
        case TokenType.ATOM: return solver.ATOM(op)
        case TokenType.NOT: return solver.NOT(op)
        case TokenType.AND: return solver.AND(op)
        case TokenType.OR: return solver.OR(op)
        case TokenType.IMPL: return solver.IMPL(op)
        case TokenType.U: return solver.U(op)
        case TokenType.X: return solver.X(op)
        case TokenType.F: return solver.F(op)
        case TokenType.R: return solver.R(op)
        case TokenType.G: return solver.G(op)
        case TokenType.W: return solver.W(op)
        case _: raise Exception("No available implementation for operator " + op) 
