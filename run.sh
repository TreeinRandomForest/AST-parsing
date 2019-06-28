#!/bin/bash

echo 'Start parsing code...'

python3 parse.py \
--file_path '../source_code_repo/test_folder/fft/pocketfft.py' \
--max_path_length 8 --max_path_width 2
