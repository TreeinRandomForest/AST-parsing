import pickle
import random


"""Split parsed data set into train, validation, test, according to the given percentage vector 
"""


# Update dictionaries from one single method
def update_dict(method, word_to_counts, path_to_counts, target_to_counts):
    target = method[0]
    if target not in target_to_counts.keys():
        target_to_counts[target] = 1
    else:
        target_to_counts[target] += 1
    for path_context in method[1:]:
        value1, path, value2 = path_context.split(',')
        if value1 not in word_to_counts.keys():
            word_to_counts[value1] = 1
        else:
            word_to_counts[value1] += 1
        if value2 not in word_to_counts.keys():
            word_to_counts[value2] = 1
        else:
            word_to_counts[value2] += 1
        if path not in path_to_counts.keys():
            path_to_counts[path] = 1
        else:
            path_to_counts[path] += 1


# Write methods from list into binary file
def write_methods(methods, path):
    with open(path, 'wb') as file:
        for line in methods:
            for item in line:
                file.write(item.encode('utf-8', 'surrogatepass') + ' '.encode('utf-8', 'surrogatepass'))
            file.write('\n'.encode('utf-8', 'surrogatepass'))


# Read methods from binary file into list
def read_methods(path):
    methods = []
    with open(path, 'rb') as file:
        for line in file:
            methods.append(line.decode('utf-8', 'surrogatepass').strip('\n').strip(' ').split(' '))
    return methods


# Get word_to_counts, path_to_counts, target_to_counts from dataset, e.g. train/validation/test
def get_dict(dataset):
    word_to_counts = {}
    path_to_counts = {}
    target_to_counts = {}
    for method in dataset:
        update_dict(method, word_to_counts, path_to_counts, target_to_counts)
    return word_to_counts, path_to_counts, target_to_counts


# Get word_to_counts, path_to_counts, target_to_counts from a given path, line by line
def get_dict_stream(path):
    word_to_counts = {}
    path_to_counts = {}
    target_to_counts = {}
    with open(path, 'rb') as file:
        for line in file:
            method = line.decode('utf-8', 'surrogatepass').strip('\n').strip(' ').split(' ')
            update_dict(method, word_to_counts, path_to_counts, target_to_counts)
    return word_to_counts, path_to_counts, target_to_counts


def split_data(seed, train_per, val_per, path_to_saved_dictionaries, path_to_saved_methods, path_to_output):
    with open(path_to_saved_dictionaries, 'rb') as file:
        N_methods = pickle.load(file)
        pickle.load(file)
        pickle.load(file)
        pickle.load(file)
        path_dictionary = pickle.load(file)

    # Load in methods
    methods = read_methods(path_to_saved_methods)

    # Split into train, validate and test
    random.seed(seed)
    random.shuffle(methods)
    train = methods[0: int(N_methods * train_per)]
    validation = methods[int(N_methods * train_per): int(N_methods * (train_per + val_per))]
    test = methods[int(N_methods * (train_per + val_per)):]

    # get dictionaries from train, validation, test
    word_to_counts_train, path_to_counts_train, target_to_counts_train = get_dict(train)
    word_to_counts_validation, path_to_counts_validation, target_to_counts_validation = get_dict(validation)
    word_to_counts_test, path_to_counts_test, target_to_counts_test = get_dict(test)

    # write train, validation, test into binary files
    write_methods(train, path_to_output+'train')
    write_methods(validation, path_to_output+'validation')
    write_methods(test, path_to_output+'test')

    # write dictionaries into binary files
    with open(path_to_output + 'dictionaries_train', 'wb') as file:
        pickle.dump(len(train), file)
        pickle.dump(word_to_counts_train, file)
        pickle.dump(path_to_counts_train, file)
        pickle.dump(target_to_counts_train, file)

    with open(path_to_output + 'dictionaries_else', 'wb') as file:
        pickle.dump(word_to_counts_validation, file)
        pickle.dump(path_to_counts_validation, file)
        pickle.dump(target_to_counts_validation, file)
        pickle.dump(word_to_counts_test, file)
        pickle.dump(path_to_counts_test, file)
        pickle.dump(target_to_counts_test, file)
        pickle.dump(path_dictionary, file)


def split_data_stream(seed, train_per, val_per, path_to_saved_dictionaries, path_to_saved_methods, path_to_output):
    with open(path_to_saved_dictionaries, 'rb') as file:
        N_methods = pickle.load(file)
        pickle.load(file)
        pickle.load(file)
        pickle.load(file)
        path_dictionary = pickle.load(file)

    # get index sets for train, validate and test
    random.seed(seed)
    indices_set = [i for i in range(0, N_methods)]
    random.shuffle(indices_set)
    train_id_set = indices_set[0: int(N_methods * train_per)]
    validate_id_set = indices_set[int(N_methods * train_per): int(N_methods * (train_per + val_per))]
    test_id_set = indices_set[int(N_methods * (train_per + val_per)):]

    # split into train, validate and test, then write into binary files
    with open(path_to_saved_methods, 'rb') as file:
        id = 0
        for line in file:
            if id in train_id_set:
                with open(path_to_output+'train', 'ab') as f:
                    f.write(line)
            if id in validate_id_set:
                with open(path_to_output+'validation', 'ab') as f:
                    f.write(line)
            if id in test_id_set:
                with open(path_to_output+'test', 'ab') as f:
                    f.write(line)
            id += 1

    # get dictionaries from train, validation, test
    word_to_counts_train, path_to_counts_train, target_to_counts_train = get_dict_stream(path_to_output+'train')
    word_to_counts_validation, path_to_counts_validation, target_to_counts_validation = get_dict_stream(path_to_output+'validation')
    word_to_counts_test, path_to_counts_test, target_to_counts_test = get_dict_stream(path_to_output+'test')

    # write dictionaries into binary files
    with open(path_to_output + 'dictionaries_train', 'wb') as file:
        pickle.dump(len(train_id_set), file)
        pickle.dump(word_to_counts_train, file)
        pickle.dump(path_to_counts_train, file)
        pickle.dump(target_to_counts_train, file)

    with open(path_to_output + 'dictionaries_else', 'wb') as file:
        pickle.dump(word_to_counts_validation, file)
        pickle.dump(path_to_counts_validation, file)
        pickle.dump(target_to_counts_validation, file)
        pickle.dump(word_to_counts_test, file)
        pickle.dump(path_to_counts_test, file)
        pickle.dump(target_to_counts_test, file)
        pickle.dump(path_dictionary, file)
