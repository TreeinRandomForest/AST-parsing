import ast
import re
from argparse import ArgumentParser


# We'd like to ignore nodes of type: Load, Store, Del
IGNORE_TYPES = ['Load', 'Store', 'Del']


def string_hashcode(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000


# strip_docstring
def strip_docstring(code_string):
    a = []
    for y in re.finditer('"""', code_string):
        a.append(y)
    output = ''
    output = output + code_string[0:a[0].start()]
    for i in range(int(len(a) / 2 - 1)):
        output = output + code_string[a[2 * i + 1].end():a[2 * i + 2].start()]
    output = output + code_string[a[len(a)-1].end():]
    return output


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


# check if a node is a leaf node
def is_leaf_node(node):
    child_nodes = [child for child in ast.iter_child_nodes(node) if type(child).__name__ not in IGNORE_TYPES]
    if not child_nodes:
        return True
    else:
        return False


def _dfs(current_node, nodes_seen, leaf_nodes_index_set, current_node_index=[-1], level=1):
    if current_node == None: return
    if type(current_node).__name__ not in IGNORE_TYPES:
        nodes_seen.append(current_node)
        current_node_index[0] += 1

        if is_leaf_node(current_node):
            leaf_nodes_index_set.append(current_node_index[0])

        # print(current_node_index[0])
        # print('-->' * (level), type(current_node).__name__, current_node_index[0])
        level += 1

        for child in ast.iter_child_nodes(current_node):
            _dfs(child, nodes_seen, leaf_nodes_index_set, current_node_index, level)


# depth-first traverse the tree, and return the list of all nodes and list of all leaf nodes indices
def dfs(root):
    nodes_seen = []
    leaf_nodes_index_set = []
    current_node_index = [-1]
    _dfs(root, nodes_seen, leaf_nodes_index_set, current_node_index)
    return nodes_seen, leaf_nodes_index_set


# get value stored in the leaf node
def get_value(node):
    for name, value in ast.iter_fields(node):
        if value is not None:
            return(value)


# find lowest common ancestor of two given nodes in the tree
def find_lca(root, node1, node2):
    if root == None: return None
    if root == node1 or root == node2: return root

    # look for lca in all subtrees
    lca_list = []
    for child_node in ast.iter_child_nodes(root):
        if child_node not in IGNORE_TYPES:
            lca_list.append(find_lca(child_node, node1, node2))

    # Remove None in the list
    lca_list = [i for i in lca_list if i != None]
    # print('for node:', type(root).__name__)
    # print(lca_list)

    # If two of the above calls returns non-None, then two nodes are present in separate subtree
    # if len(lca_list) == 2:
    if len(lca_list) >= 2:
        return root
    # If above calls return one non-None, then two nodes exit in one subtree
    if len(lca_list) == 1:
        return lca_list[0]
    return None


# extract path between two leaf nodes, given the lowest common parents
def extract_path(root, node1, node2):
    if root == None: return None
    if root == node1 or root == node2: return type(root).__name__

    # look for lca in all subtrees
    lca_list = []
    for child_node in ast.iter_child_nodes(root):
        if child_node not in IGNORE_TYPES:
            lca_list.append(extract_path(child_node, node1, node2))

    # Remove None in the list
    lca_list = [i for i in lca_list if i != None]
    # print('for node:', type(root).__name__)
    # print(lca_list)

    # If two of the above calls returns non-None, then two nodes are present in separate subtree
    # if len(lca_list) == 2:
    if len(lca_list) >= 2:
        first_str = '_'.join(lca_list[0].replace('DOWN', 'UP').split('_')[::-1])
        return first_str + '_UP_' + type(root).__name__ + '_DOWN_' + lca_list[1]
    # If above calls return one non-None, then two nodes exit in one subtree
    if len(lca_list) == 1:
        return type(root).__name__ + '_DOWN_' + lca_list[0]
    return None


# extract path contexts for single method ast (FunctionDef tree)
def extract_path_contexts_single(tree_single):
    nodes_seen, leaf_nodes_index_set = dfs(tree_single)

    N_leaf = len(leaf_nodes_index_set)
    bag_of_path_context = []
    method_name = tree_single.name
    bag_of_path_context.append(method_name)

    for i in range(N_leaf):
        for j in range(i + 1, N_leaf):
            node1 = nodes_seen[leaf_nodes_index_set[i]]
            node2 = nodes_seen[leaf_nodes_index_set[j]]
            lcp = find_lca(tree_single, node1, node2)
            path = extract_path(lcp, node1, node2)
            value1 = get_value(node1)
            value2 = get_value(node2)
            if path.split('_')[0] == type(node1).__name__:
                path_context = ','.join([str(value1), path, str(value2)])
                # path_context = ','.join([str(value1), str(string_hashcode(path)), str(value2)])
            else:
                path_context = ','.join([str(value2), path, str(value1)])
                # path_context = ','.join([str(value2), str(string_hashcode(path)), str(value1)])
            bag_of_path_context.append(path_context)
    return bag_of_path_context


# split an AST into a list of subtree nodes of type FunctionDef,
# for FunctionDef inside ClassDef, modify the method name by adding class name
def split_tree(tree):
    subtree_list = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            subtree_list.append(node)
        if isinstance(node, ast.ClassDef):
            className = node.name
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    item.name = className + '_' + item.name
                    subtree_list.append(item)
    return subtree_list


# extract path contexts from an AST generated from a script
def extract_path_contexts_file(tree):
    methods = []
    subtree_list = split_tree(tree)
    for root in subtree_list:
        temp = extract_path_contexts_single(root)
        methods.append(temp)
    return methods


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-fp', '--file_path', dest='file_path', required=False)
    arg_parser.add_argument('-dirp', '--directory_path', dest = 'directory_path', required = False)
    args = arg_parser.parse_args()

    file_path = args.file_path
    with open(file_path, 'r') as source:
        code_string = strip_docstring(source.read())
        tree = ast.parse(code_string)
    # print_tree_value(tree)
    # print_tree(tree)
    methods = extract_path_contexts_file(tree)

    print(len(methods))
    for method in methods:
        print(method[0:7], '\n\n\n')

