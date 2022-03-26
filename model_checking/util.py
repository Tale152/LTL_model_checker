class Row:
    def __init__(self, operator, boolean_array):
        self.operator = operator
        self.boolean_array = boolean_array

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

def get_first_occurrence_index_or_default(array, starting_from, value, default):
    try:
        return array.index(value, starting_from)
    except:
        return default
