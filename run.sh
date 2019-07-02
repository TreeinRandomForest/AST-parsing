#!/bin/bash

echo 'Start parsing code...'

#python3 parse.py \
#--file_path '../source_code_repo/test_folder/fft/pocketfft.py' \
#--max_path_length 8 --max_path_width 2

python3 parse.py \
--directory_path '../source_code_repo/numpy-master/numpy' \
--max_path_length 8 --max_path_width 2 \
--saved_contexts_file_name 'contexts.txt' \
--saved_dictionaries_name 'dictionaries'
