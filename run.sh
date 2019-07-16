#!/bin/bash

echo 'Start parsing code...'

#python3 parse.py \
#--file_path '../source_code_repo/numpy-master/pavement.py' \
#--max_path_length 8 --max_path_width 2 \
#--saved_contexts_file_name 't1.txt' \
#--saved_dictionaries_name 't2.txt'

python3 parse.py \
--directory_path '../source_code_repo' \
--max_path_length 8 --max_path_width 2 \
--saved_contexts_file_name 'data/parsed/contexts_all.txt' \
--saved_dictionaries_name 'data/parsed/dictionaries_all'

#python3 parse.py \
#--directory_path '../source_code_repo/test_folder' \
#--max_path_length 8 --max_path_width 2 \
#--saved_contexts_file_name 'contexts_test.txt' \
#--saved_dictionaries_name 'dictionaries_test'

echo 'Start splitting data into train, validation, test...'

python3 split.py \
--seed 10221211 \
--train_percentage 0.6 \
--validation_percentage 0.2 \
--path_to_dictionaries 'data/parsed/dictionaries_all' \
--path_to_output 'data/split/'
