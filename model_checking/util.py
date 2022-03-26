def find_row(op, computed_rows):
    return next(filter(lambda r: r.operator == op, computed_rows))

def get_left_child_boolean_array(op, computed_rows):
    return find_row(op.children()[0], computed_rows).boolean_array

def get_right_child_boolean_array(op, computed_rows):
    return find_row(op.children()[1], computed_rows).boolean_array

def get_child_boolean_array(op, computed_rows):
    return get_left_child_boolean_array(op, computed_rows)

def create_array_with_value(size, value):
    return [value for _ in range(size)]

def true_array(size):
    return create_array_with_value(size, True)
