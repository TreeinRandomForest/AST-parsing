import pickle
from Utils import string_hashcode


class Contexts(object):
    """
    Store extracted path contexts in this class object defined
    """
    def __init__(self, ml, mw):
        self.path_dictionary = {}
        self.path_to_counts = {}
        self.word_to_counts = {}
        self.target_to_counts = {}
        self.N_methods = 0
        self.methods = []
        self.max_path_length = ml
        self.max_path_width = mw

    def update_dictionaries(self, path, hashed_path, word1, word2):
        if hashed_path not in self.path_dictionary.keys():
            self.path_dictionary[hashed_path] = path
            self.path_to_counts[hashed_path] = 1
        else:
            self.path_to_counts[hashed_path] += 1
        if word1 not in self.word_to_counts.keys():
            self.word_to_counts[word1] = 1
        else:
            self.word_to_counts[word1] += 1
        if word2 not in self.word_to_counts.keys():
            self.word_to_counts[word2] = 1
        else:
            self.word_to_counts[word2] += 1

    def append_contexts(self, methods_in_file):
        self.N_methods += len(methods_in_file)
        for method in methods_in_file:
            if len(method) <= 1:
                print(method)
                print('fffffffffffffffffffffffffffffffffffffff')
                continue
            hashed_method = [method[0]]
            target_name = method[0]
            if target_name not in self.target_to_counts.keys():
                self.target_to_counts[target_name] = 1
            else:
                self.target_to_counts[target_name] += 1
            for context in method[1:]:
                context_array = context.split(',')
                if len(context_array) != 3:
                    continue
                path = context_array[1]
                word1 = context_array[0]
                word2 = context_array[2]
                hashed_path = str(string_hashcode(path))
                hashed_context = ','.join([word1, hashed_path, word2])
                hashed_method.append(hashed_context)
                self.update_dictionaries(path, hashed_path, word1, word2)
            self.methods.append(hashed_method)

    def print(self, N):
        """Print bag of contexts for first N lines of methods
        """
        print(self.N_methods)
        n = 0
        for method in self.methods:
            if n < N:
                print(method, '\n\n\n')
                n += 1

    def write(self, output_file):
        with open(output_file, 'a+') as f:
            if self.N_methods <=1:
                f.write(" ".join(self.methods).replace('\n', '') + '\n')
            else:
                for line in self.methods:
                    f.write(" ".join(line).replace('\n', '') + '\n')
        print('Contexts saved!')

    def save_dictionaries(self, output_file2):
        with open(output_file2, 'wb') as f:
            pickle.dump(self.path_dictionary, f)
            pickle.dump(self.word_to_counts, f)
            pickle.dump(self.path_to_counts, f)
            pickle.dump(self.target_to_counts, f)
            pickle.dump(self.N_methods, f)
            pickle.dump(self.methods, f)
            print('Dictionaries saved!')
