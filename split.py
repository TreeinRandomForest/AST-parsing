from SplitData import SplitData
from argparse import ArgumentParser

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--seed', dest='seed', required=True)
    arg_parser.add_argument('--train_percentage', dest='train_per', required=True)
    arg_parser.add_argument('--validation_percentage', dest='validation_per', required=True)
    arg_parser.add_argument('--path_to_dictionaries', dest='path_to_dictionaries', required=True)
    arg_parser.add_argument('--path_to_output', dest='path_to_output', required=True)

    args = arg_parser.parse_args()
    # split data
    SplitData(int(args.seed), float(args.train_per), float(args.validation_per), args.path_to_dictionaries,\
              args.path_to_output)
