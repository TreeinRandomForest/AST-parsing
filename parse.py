import ast
import os
from argparse import ArgumentParser
from Utils import strip_docstring
from ExtractPathContexts import extract_path_contexts_file


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-fp', '--file_path', dest='file_path', required=False)
    arg_parser.add_argument('-dirp', '--directory_path', dest = 'directory_path', required=False)
    arg_parser.add_argument('-ml', '--max_path_length', dest='max_path_length', required=True)
    arg_parser.add_argument('-mw', '--max_path_width', dest = 'max_path_width', required=True)
    args = arg_parser.parse_args()

    file_path = args.file_path
    directory_path = args.directory_path
    max_path_length = int(args.max_path_length)
    max_path_width = int(args.max_path_width)

    path_dictionary = {}

    if file_path is not None:
        with open(file_path, 'r') as source:
            code_string = strip_docstring(source.read())
            tree = ast.parse(code_string)
            # print_tree_value(tree)
            # print_tree(tree)
            methods = extract_path_contexts_file(tree, max_path_width, max_path_length)
            print(len(methods))
            for method in methods:
                print(method[0:10], '\n\n\n')

    if directory_path is not None:
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in [f for f in filenames if f.endswith(".py")]:
                print(os.path.join(dirpath, filename))

