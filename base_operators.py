def create_array_with_value(size, value):
    result = []
    for i in range(size):
        result.append(value)
    return result

def U_operator_non_determinism(first, second, i, loop_size, current_results):
    n_states = len(first)
    for j in range(i + 1, n_states + 1):
        if j == n_states:
            actual_j = n_states - loop_size
            if len(current_results) <= actual_j:
                return create_array_with_value(n_states - i, False)
            else:
                if current_results[actual_j] == True:
                    return create_array_with_value(j - i, True)
                else:
                    return create_array_with_value(j - i, False)
        else:
            if second[j] == True:
                return create_array_with_value(j - i + 1, True)
            elif first[i] == False:
                return create_array_with_value(j - i + 1, False)

def U_operator(first, second, loop_size):
    bool_row = []
    i = 0
    while i < len(first):
        if second[i] == True:
            bool_row.append(True)
            i += 1
        elif first[i] == False:
            bool_row.append(False)
            i += 1
        else:
            r = U_operator_non_determinism(first, second, i, loop_size, bool_row)
            i += len(r)
            bool_row += r
    return bool_row

def X_operator(child, loop_size):
    loop_index = len(child) - loop_size
    result = child.copy()
    result.append(child[loop_index])
    result.pop(0)
    return result