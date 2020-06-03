import ast
import os
from argparse import ArgumentParser
from Utils import strip_docstring
from ExtractPathContexts import extract_path_contexts_file
from StoreExtracted import StoreExtracted


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-fp', '--file_path', dest='file_path', required=False)
    arg_parser.add_argument('-dirp', '--directory_path', dest = 'directory_path', required=False)
    arg_parser.add_argument('-ml', '--max_path_length', dest='max_path_length', required=True)
    arg_parser.add_argument('-mw', '--max_path_width', dest='max_path_width', required=True)
    arg_parser.add_argument('-smfn', '--saved_methods_filename', dest='saved_methods_filename', required=True)
    arg_parser.add_argument('-sdfn', '--saved_dictionaries_filename', dest='saved_dictionaries_filename', required=True)
    args = arg_parser.parse_args()

    file_path = args.file_path
    directory_path = args.directory_path
    max_path_length = int(args.max_path_length)
    max_path_width = int(args.max_path_width)

    StoreExtracted = StoreExtracted(max_path_length, max_path_width)
    N_syntax_error = 0
    N_files = 0

    if os.path.exists(args.saved_methods_filename):
        os.remove(args.saved_methods_filename)

    if file_path is not None:
        with open(file_path, 'r') as source:
            code_string = strip_docstring(source.read())
            try:
                tree = ast.parse(code_string)
                # print_tree_value(tree)
                # print_tree(tree)
                methods_in_file = extract_path_contexts_file(tree, max_path_width, max_path_length)
                StoreExtracted.update_hash_save(methods_in_file, args.saved_methods_filename)
                #StoreExtracted.print(10)
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
                        StoreExtracted.update_hash_save(methods_in_file, args.saved_methods_filename)
                    except SyntaxError:
                        N_syntax_error += 1
                StoreExtracted.print(0)

    if os.path.exists(args.saved_dictionaries_filename):
        os.remove(args.saved_dictionaries_filename)
    StoreExtracted.save_dictionaries(args.saved_dictionaries_filename)

    print('Total number of scripts with syntax_error', N_syntax_error)
    print('Total number of files:', N_files)
    print('Extracted:', StoreExtracted.N_methods, 'methods')
    StoreExtracted.print(5)


