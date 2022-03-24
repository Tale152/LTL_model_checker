def getAstMaxDepth(root):
    return getAstMaxDepthRecursion(root, 0)

def getAstMaxDepthRecursion(node, counter):
    if node.arity() == 0:
        return counter
    else:
        childrenDepth = []
        for i in range(node.arity()):
            childrenDepth.append(getAstMaxDepthRecursion(node.children()[i], counter + 1))
        return max(childrenDepth)

def getNodesFromLevel(root, level):
    if level == 0:
        return [root]
    else:
        return getNodesFromLevelRecursion(root, 0, level)

def getNodesFromLevelRecursion(node, currentLevel, levelToReach):
    if(currentLevel == levelToReach - 1):
        return node.children()
    else:
        result = []
        for i in range(node.arity()):
            result = result + getNodesFromLevelRecursion(node.children()[i], currentLevel + 1, levelToReach)
        return result

def create_rows_array(root):
    result = []
    maxDepth = getAstMaxDepth(root)
    for i in reversed(range(maxDepth + 1)):
        result = result + getNodesFromLevel(root, i)
    return result
