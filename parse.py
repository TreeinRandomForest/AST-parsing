import ast
import os
from argparse import ArgumentParser
from Utils import strip_docstring
from ExtractPathContexts import extract_path_contexts_file
from Contexts import Contexts


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-fp', '--file_path', dest='file_path', required=False)
    arg_parser.add_argument('-dirp', '--directory_path', dest = 'directory_path', required=False)
    arg_parser.add_argument('-ml', '--max_path_length', dest='max_path_length', required=True)
    arg_parser.add_argument('-mw', '--max_path_width', dest = 'max_path_width', required=True)
    arg_parser.add_argument('-scf', '--saved_contexts_file_name', dest = 'saved_contexts_file_name', required=True)
    arg_parser.add_argument('-sdic', '--saved_dictionaries_name', dest = 'saved_dictionaries_name', required=True)
    args = arg_parser.parse_args()

    file_path = args.file_path
    directory_path = args.directory_path
    max_path_length = int(args.max_path_length)
    max_path_width = int(args.max_path_width)

    Contexts = Contexts(max_path_length, max_path_width)
    N_syntax_error = 0
    N_files = 0

    if file_path is not None:
        with open(file_path, 'r') as source:
            code_string = strip_docstring(source.read())
            try:
                tree = ast.parse(code_string)
                # print_tree_value(tree)
                # print_tree(tree)
                methods_in_file = extract_path_contexts_file(tree, max_path_width, max_path_length)
                Contexts.append_contexts(methods_in_file)
                Contexts.print(10)
                N_files += 1
            except SyntaxError:
                N_syntax_error += 1

    if directory_path is not None:
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in [f for f in filenames if f.endswith(".py")]:
                file_path = os.path.join(dirpath, filename)
                print(file_path)
                N_files += 1
                with open(file_path, 'r') as source:
                    code_string = strip_docstring(source.read())
                    try:
                        tree = ast.parse(code_string)
                        # print_tree_value(tree)
                        # print_tree(tree)
                        methods_in_file = extract_path_contexts_file(tree, max_path_width, max_path_length)
                        Contexts.append_contexts(methods_in_file)
                    except SyntaxError:
                        N_syntax_error += 1
                Contexts.print(0)

    if os.path.exists(args.saved_contexts_file_name):
        os.remove(args.saved_contexts_file_name)
    if os.path.exists(args.saved_dictionaries_name):
        os.remove(args.saved_dictionaries_name)

    Contexts.write(args.saved_contexts_file_name)
    Contexts.save_dictionaries(args.saved_dictionaries_name)

    print('Total number of scripts with syntax_error', N_syntax_error)
    print('Total number of files:', N_files)
    print('Extracted:', Contexts.N_methods, 'methods')
    Contexts.print(5)


