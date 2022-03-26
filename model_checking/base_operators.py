from model_checking.util import *

class BaseOperatorsSolver:

    def __init__(self, loop_size):
        self.loop_size = loop_size

    def U_operator_non_determinism(self, first, second, i, current_results):
        n_states = len(first)
        for j in range(i + 1, n_states + 1):
            if j == n_states:
                actual_j = n_states - self.loop_size
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

    def U(self, first, second):
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
                r = self.U_operator_non_determinism(first, second, i, bool_row)
                i += len(r)
                bool_row += r
        return bool_row

    def X(self, child):
        loop_index = len(child) - self.loop_size
        result = child.copy()
        result.append(child[loop_index])
        result.pop(0)
        return result

    def OR(self, left_child, right_child):
        result = []
        for i in range(len(left_child)):
            result.append(left_child[i] or right_child[i])
        return result

    def NOT(self, child):
        result = child.copy()
        for i in range(len(result)):
            result[i] = not result[i]
        return result
