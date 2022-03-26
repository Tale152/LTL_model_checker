from interface import parse, getpath
from model_checking.ordered_operators_extractor import extract_ordered_operators_array
from model_checking.ltl_evaluator import evaluate

parsed = parse("G(employee_right -> (!employee_left && !employee_trans))")

paths = [
    "./paths/path0.txt",
    "./paths/path1.txt",
    "./paths/path2.txt",
    "./paths/path3.txt",
    "./paths/path4.txt",
    "./paths/path5.txt",
    "./paths/path6.txt",
    "./paths/path7.txt"
]
for p in paths:
    path = getpath(p)
    print(evaluate(extract_ordered_operators_array(parsed), path.path, path.loop))
