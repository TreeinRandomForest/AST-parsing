#!/bin/bash

echo 'Start parsing code...'

#python3 parse.py \
#--file_path '../source_code_repo/numpy-master/pavement.py' \
#--max_path_length 8 --max_path_width 2 \
#--saved_contexts_file_name 't1.txt' \
#--saved_dictionaries_name 't2.txt'

python3 parse.py \
--directory_path '../source_code_repo/numpy-master/' \
--max_path_length 8 --max_path_width 2 \
--saved_contexts_file_name 'contexts_all.txt' \
--saved_dictionaries_name 'dictionaries_all'
