from SplitData import split_data, split_data_stream
from argparse import ArgumentParser
import os

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--seed', dest='seed', required=True)
    arg_parser.add_argument('--train_percentage', dest='train_per', required=True)
    arg_parser.add_argument('--validation_percentage', dest='validation_per', required=True)
    arg_parser.add_argument('--path_to_saved_dictionaries', dest='path_to_saved_dictionaries', required=True)
    arg_parser.add_argument('--path_to_saved_methods', dest='path_to_saved_methods', required=True)
    arg_parser.add_argument('--path_to_output', dest='path_to_output', required=True)

    args = arg_parser.parse_args()
    if os.path.exists(args.path_to_output+'train'):
        os.remove(args.path_to_output+'train')
    if os.path.exists(args.path_to_output+'test'):
        os.remove(args.path_to_output+'test')
    if os.path.exists(args.path_to_output+'validation'):
        os.remove(args.path_to_output+'validation')
    # split data
    split_data_stream(int(args.seed), float(args.train_per), float(args.validation_per), args.path_to_saved_dictionaries,\
              args.path_to_saved_methods, args.path_to_output)
