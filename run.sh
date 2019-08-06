#!/bin/bash

DATA_DIR='Data'
#DATASET='data_small'
#DATASET='data_numpy'
#DATASET='data_numpy_pandas_sklearn'
DATASET='data_large'

echo 'Start parsing code...'

#python3 parse.py \
#--file_path '../source_code_repo/pandas-master/pandas/tests/io/pytables/test_pytables.py' \
#--max_path_length 8 --max_path_width 2 \
#--saved_methods_filename 't1' \
#--saved_dictionaries_filename 't2'

python3 parse.py \
--directory_path '/home/xiaojzhu/.local/lib/python3.7/site-packages' \
--max_path_length 8 --max_path_width 2 \
--saved_methods_filename ${DATA_DIR}/${DATASET}/parsed/methods \
--saved_dictionaries_filename ${DATA_DIR}/${DATASET}/parsed/dictionaries

#--directory_path '../source_code_repo/numpy-master/numpy/polynomial' \
#--directory_path '../source_code_repo/numpy-master' \
#--directory_path '../source_code_repo' \
#--directory_path '/home/xiaojzhu/.local/lib/python3.7/site-packages' \

python3 split.py \
--seed 10221211 \
--train_percentage 0.8 \
--validation_percentage 0.1 \
--path_to_saved_dictionaries ${DATA_DIR}/${DATASET}/parsed/dictionaries \
--path_to_saved_methods ${DATA_DIR}/${DATASET}/parsed/methods \
--path_to_output ${DATA_DIR}/${DATASET}/split/

echo 'Finished!'
