#!/bin/bash

SOURCE_DIR=$1
SOURCE_FILE=$2
NAME=$3

USERNAME=sdmay23_16
HOST=berk.ece.iastate.edu

cd ${SOURCE_DIR}
scp $SOURCE_DIR$SOURCE_FILE ${USERNAME}@${HOST}:~/testing_workspace/Data/
ssh -l ${USERNAME} ${HOST} "cd testing_workspace/; source tensorflow/roy-venv/bin/activate; ./Restored_model_test.py >> results_${NAME}.txt; deactivate" >> ${NAME}/log_${NAME}.txt
scp ${USERNAME}@${HOST}:~/testing_workspace/results_${NAME}.txt ${SOURCE_DIR}/${NAME}