#!/bin/bash

#############
# ARGUMENTS #
#############
# Working directory / source directory
SOURCE_DIR=$1
# Name of the attack test run
NAME=$2

source ./config.sh

#########
# START #
#########

cd ${SOURCE_DIR}
scp $SOURCE_DIR$NAME/X_attack_test_15.csv ${MLS_USERNAME}@${MLS_HOST}:${MLS_WORKSPACE}Data/
ssh -l ${MLS_USERNAME} ${MLS_HOST} "cd ${MLS_WORKSPACE}; source tensorflow/roy-venv/bin/activate; ./Restored_model_test.py >> results_${NAME}.txt; deactivate"
scp ${MLS_USERNAME}@${MLS_HOST}:${MLS_WORKSPACE}results_${NAME}.txt ${SOURCE_DIR}/${NAME}/results.txt