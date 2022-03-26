from model_checking.util import *

class BaseOperatorsSolver:

    def __init__(self, loop_size):
        self.loop_size = loop_size

    def NOT(self, child):
        result = child.copy()
        for i in range(len(result)):
            result[i] = not result[i]
        return result

    def OR(self, left_child, right_child):
        result = []
        for i in range(len(left_child)):
            result.append(left_child[i] or right_child[i])
        return result

    def X(self, child):
        result = child.copy()
        loop_start_index = len(child) - self.loop_size
        result.append(child[loop_start_index])
        result.pop(0)
        return result

    def U(self, first_child, second_child):
        # initializing array with "not determinated" values (add one more element for replicating the start of lasso loop)
        result = create_array_with_value(len(first_child) + 1, "nd")

        # resolving result where immediately possible
        for i in range(len(first_child)):
            if second_child[i] == True:
                result[i] = True
            elif first_child[i] == False:
                result[i] = False
        loop_start_index = len(first_child) - self.loop_size
        result[-1] = result[loop_start_index] # synchronizing beginning of lazo loop and it's copy at the end of array result
        
        # resolving still not determinated values using previously solved values
        while(result.count("nd") > 0):
            ND_first_index = result.index("nd")
            True_first_index = get_first_occurrence_index_or_default(result, ND_first_index, True, len(result))
            False_first_index = get_first_occurrence_index_or_default(result, ND_first_index, False, len(result))
            result[ND_first_index] = not ((True_first_index == False_first_index) or (False_first_index < True_first_index))
            if ND_first_index == loop_start_index:
                result[-1] = result[loop_start_index] # synchronizing beginning of lazo loop and it's copy at the end of array result

        result.pop(-1) # removing copy of beginning of lazo loop since it isn't needed anymore
        return result
