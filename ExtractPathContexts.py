import re
import ast

# We'd like to ignore nodes of type: Load, Store, Del
IGNORE_TYPES = ['Load', 'Store', 'Del']


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
            if isinstance(value, list):
                value_str = [str(i).replace(' ', '') for i in value]
                res = '|'.join(value_str).strip().replace('\n', '')
            else:
                #print(type(value))
                res = str(value).strip().replace(' ', '').replace('\n', '')
            #print (res.encode('utf-8'))
            return res


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
def extract_path_contexts_single(tree_single, max_path_width, max_path_length):
    nodes_seen, leaf_nodes_index_set = dfs(tree_single)

    N_leaf = len(leaf_nodes_index_set)
    bag_of_path_context = []
    method_name = tree_single.name
    bag_of_path_context.append(method_name)

    for i in range(N_leaf):
        for j in range(i + 1, N_leaf):
            if abs(i - j) > max_path_width:
                continue
            node1 = nodes_seen[leaf_nodes_index_set[i]]
            node2 = nodes_seen[leaf_nodes_index_set[j]]
            lcp = find_lca(tree_single, node1, node2)
            path = extract_path(lcp, node1, node2)
            path_length = len(re.split('_UP_|_DOWN_', path)) - 1
            if path_length > max_path_length:
                continue
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
                    item.name = className + '||' + item.name
                    subtree_list.append(item)
    return subtree_list


# extract path contexts from an AST generated from a script
def extract_path_contexts_file(tree, max_path_width, max_path_length):
    methods = []
    subtree_list = split_tree(tree)
    for root in subtree_list:
        temp = extract_path_contexts_single(root, max_path_width, max_path_length)
        methods.append(temp)
    return methods


# import ast
# import re
# from Utils import string_hashcode
#
#
# # We'd like to ignore nodes of type: Load, Store, Del
# IGNORE_TYPES = ['Load', 'Store', 'Del']
#
#
# class ExtractPathContexts(object):
#     def __init__(self, max_path_length, max_path_width):
#         self.path_dictionary = {}
#         self.methods_contexts = []
#         self.max_path_length = max_path_length
#         self.max_path_width = max_path_width
#
#     @staticmethod
#     def print_tree_value(tree, level = 0):
#         """ print all ast fields except None
#         """
#         if isinstance(tree, ast.AST):
#             print('-->'*(level), type(tree).__name__)
#         elif tree != None:
#             print('-->'*(level), tree, "*")
#             return
#         else:
#             return
#         #else:
#         #    print('-->'*(level), tree, "*")
#         #    return
#         level += 1
#         for child_name, child_obj in ast.iter_fields(tree):
#             if isinstance(child_obj, list):
#                 for item in child_obj:
#                     ExtractPathContexts.print_tree_value(item, level=level)
#             else:
#                 ExtractPathContexts.print_tree_value(child_obj, level=level)
#         return
#
#     @staticmethod
#     def print_tree(tree, level=0):
#         """ print only the ast node type
#         """
#         if isinstance(tree, ast.AST):
#             print('-->'*level, type(tree).__name__)
#         else:
#             print('-->'*level, tree, "*")
#             return
#         level = level + 1
#         for child_obj in ast.iter_child_nodes(tree):
#             ExtractPathContexts.print_tree(child_obj, level=level)
#         return
#
#     @staticmethod
#     def is_leaf_node(node):
#         """check if a node is a leaf node
#         """
#         child_nodes = [child for child in ast.iter_child_nodes(node) if type(child).__name__ not in IGNORE_TYPES]
#         if not child_nodes:
#             return True
#         else:
#             return False
#
#     @staticmethod
#     def _dfs(current_node, nodes_seen, leaf_nodes_index_set, current_node_index=[-1], level=1):
#         if current_node == None: return
#         if type(current_node).__name__ not in IGNORE_TYPES:
#             nodes_seen.append(current_node)
#             current_node_index[0] += 1
#
#             if ExtractPathContexts.is_leaf_node(current_node):
#                 leaf_nodes_index_set.append(current_node_index[0])
#
#             # print(current_node_index[0])
#             # print('-->' * (level), type(current_node).__name__, current_node_index[0])
#             level += 1
#
#             for child in ast.iter_child_nodes(current_node):
#                 ExtractPathContexts._dfs(child, nodes_seen, leaf_nodes_index_set, current_node_index, level)
#
#     @staticmethod
#     def dfs(root):
#         """depth-first traverse the tree, and return the list of all nodes and list of all leaf nodes indices
#         """
#         nodes_seen = []
#         leaf_nodes_index_set = []
#         current_node_index = [-1]
#         ExtractPathContexts._dfs(root, nodes_seen, leaf_nodes_index_set, current_node_index)
#         return nodes_seen, leaf_nodes_index_set
#
#     @staticmethod
#     def get_value(node):
#         """get value stored in the leaf node
#         """
#         for name, value in ast.iter_fields(node):
#             if value is not None:
#                 return value
#
#     @staticmethod
#     def find_lca(root, node1, node2):
#         """find lowest common ancestor of two given nodes in the tree
#         """
#         if root == None: return None
#         if root == node1 or root == node2: return root
#
#         # look for lca in all subtrees
#         lca_list = []
#         for child_node in ast.iter_child_nodes(root):
#             if child_node not in IGNORE_TYPES:
#                 lca_list.append(ExtractPathContexts.find_lca(child_node, node1, node2))
#
#         # Remove None in the list
#         lca_list = [i for i in lca_list if i != None]
#         # print('for node:', type(root).__name__)
#         # print(lca_list)
#
#         # If two of the above calls returns non-None, then two nodes are present in separate subtree
#         # if len(lca_list) == 2:
#         if len(lca_list) >= 2:
#             return root
#         # If above calls return one non-None, then two nodes exit in one subtree
#         if len(lca_list) == 1:
#             return lca_list[0]
#         return None
#
#     @staticmethod
#     def extract_path(root, node1, node2):
#         """extract path between two leaf nodes, given the lowest common parents
#         """
#         if root == None: return None
#         if root == node1 or root == node2: return type(root).__name__
#
#         # look for lca in all subtrees
#         lca_list = []
#         for child_node in ast.iter_child_nodes(root):
#             if child_node not in IGNORE_TYPES:
#                 lca_list.append(ExtractPathContexts.extract_path(child_node, node1, node2))
#
#         # Remove None in the list
#         lca_list = [i for i in lca_list if i != None]
#         # print('for node:', type(root).__name__)
#         # print(lca_list)
#
#         # If two of the above calls returns non-None, then two nodes are present in separate subtree
#         # if len(lca_list) == 2:
#         if len(lca_list) >= 2:
#             first_str = '_'.join(lca_list[0].replace('DOWN', 'UP').split('_')[::-1])
#             return first_str + '_UP_' + type(root).__name__ + '_DOWN_' + lca_list[1]
#         # If above calls return one non-None, then two nodes exit in one subtree
#         if len(lca_list) == 1:
#             return type(root).__name__ + '_DOWN_' + lca_list[0]
#         return None
#
#     def extract_path_contexts_single(tree_single, self.max_path_width, self.max_path_length):
#         """ extract path contexts for single method ast (FunctionDef tree)
#         """
#         nodes_seen, leaf_nodes_index_set = ExtractPathContexts.dfs(tree_single)
#
#         N_leaf = len(leaf_nodes_index_set)
#         bag_of_path_context = []
#         method_name = tree_single.name
#         bag_of_path_context.append(method_name)
#
#         for i in range(N_leaf):
#             for j in range(i + 1, N_leaf):
#                 if abs(i - j) > max_path_width:
#                     continue
#                 node1 = nodes_seen[leaf_nodes_index_set[i]]
#                 node2 = nodes_seen[leaf_nodes_index_set[j]]
#                 lcp = find_lca(tree_single, node1, node2)
#                 path = extract_path(lcp, node1, node2)
#                 path_length = len(re.split('_UP_|_DOWN_', path)) - 1
#                 if path_length > max_path_length:
#                     continue
#                 value1 = get_value(node1)
#                 value2 = get_value(node2)
#                 if path.split('_')[0] == type(node1).__name__:
#                     path_context = ','.join([str(value1), path, str(value2)])
#                     # path_context = ','.join([str(value1), str(string_hashcode(path)), str(value2)])
#                 else:
#                     path_context = ','.join([str(value2), path, str(value1)])
#                     # path_context = ','.join([str(value2), str(string_hashcode(path)), str(value1)])
#                 bag_of_path_context.append(path_context)
#         return bag_of_path_context
#
#     @staticmethod
#
#     # split an AST into a list of subtree nodes of type FunctionDef,
#     # for FunctionDef inside ClassDef, modify the method name by adding class name
#     def split_tree(tree):
#         subtree_list = []
#         for node in tree.body:
#             if isinstance(node, ast.FunctionDef):
#                 subtree_list.append(node)
#             if isinstance(node, ast.ClassDef):
#                 className = node.name
#                 for item in node.body:
#                     if isinstance(item, ast.FunctionDef):
#                         item.name = className + '_' + item.name
#                         subtree_list.append(item)
#         return subtree_list
#
#
#     # extract path contexts from an AST generated from a script
#     def extract_path_contexts_file(tree, max_path_width, max_path_length):
#         methods = []
#         subtree_list = split_tree(tree)
#         for root in subtree_list:
#             temp = extract_path_contexts_single(root, max_path_width, max_path_length)
#             methods.append(temp)
#         return methods
