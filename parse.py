import ast
import os
from argparse import ArgumentParser
from Utils import strip_docstring, string_hashcode
from ExtractPathContexts import extract_path_contexts_file
import pickle


class Contexts(object):
    """
    Store extracted path contexts
    """
    def __init__(self, ml, mw):
        self.path_dictionary = {}
        self.path_counts = {}
        self.value_counts = {}
        self.N_methods = 0
        self.methods = []
        self.max_path_length = ml
        self.max_path_width = mw

    def update_dictionaries(self, path, hashed_path, word1, word2):
        if hashed_path not in self.path_dictionary.keys():
            self.path_dictionary[hashed_path] = path
            self.path_counts[hashed_path] = 1
        else:
            self.path_counts[hashed_path] += 1
        if word1 not in self.value_counts.keys():
            self.value_counts[word1] = 1
        else:
            self.value_counts[word1] += 1
        if word2 not in self.value_counts.keys():
            self.value_counts[word2] = 1
        else:
            self.value_counts[word2] += 1

    def append_contexts(self, methods_in_file):
        self.N_methods += len(methods_in_file)
        for method in methods_in_file:
            hashed_method = [method[0]]
            for context in method[1:]:
                context_array = context.split(',')
                path = context_array[1]
                word1 = context_array[0]
                word2 = context_array[2]
                hashed_path = str(string_hashcode(path))
                hashed_context = ','.join([word1, hashed_path, word2])
                hashed_method.append(hashed_context)
                self.update_dictionaries(path, hashed_path, word1, word2)
            self.methods.append(hashed_method)

    def print(self, N):
        print(self.N_methods)
        n = 0
        for method in Contexts.methods:
            if n < N:
                print(method, '\n\n\n')
                n += 1

    def write(self, output_file):
        with open(output_file, 'a+') as f:
            if self.N_methods <=1:
                f.write(" ".join(self.methods) + '\n')
            else:
                for line in self.methods:
                    f.write(" ".join(line) + "\n")
        print('Contexts saved!')

    def save_dictionaries(self, output_file2):
        with open(output_file2, 'wb') as f:
            pickle.dump(self.path_dictionary, f)
            pickle.dump(self.value_counts, f)
            pickle.dump(self.path_counts, f)
            pickle.dump(self.N_methods, f)
            print('Dictionaries saved!')



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
            except SyntaxError:
                N_syntax_error += 1

    if directory_path is not None:
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in [f for f in filenames if f.endswith(".py")]:
                file_path = os.path.join(dirpath, filename)
                print(file_path)
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

    Contexts.write(args.saved_contexts_file_name)
    Contexts.save_dictionaries(args.saved_dictionaries_name)
    print('Total number of scripts with syntax_error', N_syntax_error)


