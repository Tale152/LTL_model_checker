from interface import parse, getpath
from model_checking.rows_extractor import create_rows_array
from model_checking.ltl_evaluator import evaluate

parsed = parse("G(employee_right -> (!employee_left && !employee_trans))")

path = getpath("./paths/path0.txt")
print(evaluate(create_rows_array(parsed), path.path, path.loop))
