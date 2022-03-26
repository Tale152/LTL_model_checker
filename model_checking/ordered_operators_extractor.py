def __descend_ast(node, result):
    for c in node.children(): __descend_ast(c, result)
    result.append(node)

def extract_ordered_operators_array(root):
    result = []
    __descend_ast(root, result)
    return result
