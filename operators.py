from Row import Row

def find_row(op, computed_rows):
    for r in computed_rows:
        if r.operator == op:
            return r
    raise Exception("operator from previously computed rows not found: " + str(op.value))

def solve_not(op, computed_rows):
    print("here")
    child = find_row(op.children()[0], computed_rows)
    bool_row = []
    for b in child.boolean_array:
        bool_row.append(not b)
    return Row(op, bool_row)

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