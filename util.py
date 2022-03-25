def find_row(op, computed_rows):
    for r in computed_rows:
        if r.operator == op:
            return r
    raise Exception("operator from previously computed rows not found: " + str(op.value))

def get_left_child_boolean_array(op, computed_rows):
    return find_row(op.children()[0], computed_rows).boolean_array

def get_right_child_boolean_array(op, computed_rows):
    return find_row(op.children()[1], computed_rows).boolean_array

def get_child_boolean_array(op, computed_rows):
    return get_left_child_boolean_array(op, computed_rows)

def create_array_with_value(size, value):
    result = []
    for i in range(size):
        result.append(value)
    return result