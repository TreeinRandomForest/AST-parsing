import ast


# print all ast fields except None
def print_tree_value(tree, level = 0):
    if isinstance(tree, ast.AST):
        print('-->'*(level), type(tree).__name__)
    elif tree != None:
        print('-->'*(level), tree, "*")
        return
    else:
        return
    #else:
    #    print('-->'*(level), tree, "*")
    #    return
    level += 1
    for child_name, child_obj in ast.iter_fields(tree):
        if isinstance(child_obj, list):
            for item in child_obj:
                print_tree_value(item, level = level)
        else:
            print_tree_value(child_obj, level = level)
    return


# print only the ast node type
def print_tree(tree, level = 0):
    if isinstance(tree, ast.AST):
        print('-->'*(level), type(tree).__name__)
    else:
        print('-->'*(level), tree, "*")
        return
    level = level + 1
    for child_obj in ast.iter_child_nodes(tree):
        print_tree(child_obj, level = level)
    return



if __name__ == '__main__':
    with open('example.py', 'r') as source:
        tree = ast.parse(source.read())
    print_tree_value(tree)
    print_tree(tree)



