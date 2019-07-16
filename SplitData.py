import pickle
import random


"""Split parsed data set into train, validation, test, according to the given percentage vector 
"""


# Update word_to_counts, path_to_counts, target_to_counts for dataset, e.g. train/validation/test
def SplitDict(dataset):
    word_to_counts = {}
    path_to_counts = {}
    target_to_counts = {}
    for method in dataset:
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
    return word_to_counts, path_to_counts, target_to_counts


def SplitData(seed, train_per, val_per, path_to_saved_dictionaries, path_to_output):
    with open(path_to_saved_dictionaries, 'rb') as file:
        path_dictionary = pickle.load(file)
        word_to_counts = pickle.load(file)
        path_to_counts = pickle.load(file)
        target_to_counts = pickle.load(file)
        N_methods = pickle.load(file)
        contexts = pickle.load(file)

    # split into train, validate and test
    random.seed(seed)
    random.shuffle(contexts)
    train = contexts[0: int(N_methods * train_per)]
    validation = contexts[int(N_methods * train_per): int(N_methods * (train_per + val_per))]
    test = contexts[int(N_methods * (train_per + val_per)):]

    # split saved dictionaries into train, validation, test
    word_to_counts_train, path_to_counts_train, target_to_counts_train = SplitDict(train)
    word_to_counts_validation, path_to_counts_validation, target_to_counts_validation = SplitDict(validation)
    word_to_counts_test, path_to_counts_test, target_to_counts_test = SplitDict(test)

    # write into binary files
    with open(path_to_output + 'train', 'wb') as file:
        pickle.dump(train, file)
        pickle.dump(len(train), file)
    with open(path_to_output + 'test', 'wb') as file:
        pickle.dump(test, file)
        pickle.dump(len(test), file)
    with open(path_to_output + 'validation', 'wb') as file:
        pickle.dump(validation, file)
        pickle.dump(len(validation), file)

    with open(path_to_output + 'dictionaries_train', 'wb') as file:
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

