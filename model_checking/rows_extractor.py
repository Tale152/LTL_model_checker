def descend_ast(node, result):
    for c in node.children(): descend_ast(c, result)
    result.append(node)

def create_rows_array(root):
    result = []
    descend_ast(root, result)
    return result
