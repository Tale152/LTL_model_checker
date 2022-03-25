from interface import parse, getpath
from rows_extractor import create_rows_array
from ltl_evaluator import evaluate

parsed = parse("(employee_left || employee_trans || employee_right)")

path = getpath("./paths/path0.txt")
print(evaluate(create_rows_array(parsed), path.path, path.loop))
