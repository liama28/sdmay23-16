#!/bin/bash
#sh scp_helper.sh ~/Desktop/Senior_Design/sdmay23-16/Liam_experiments/ Source_test.c testrun3423 3 1

#############
# ARGUMENTS #
#############
# Working directory / source directory
SOURCE_DIR=$1
# Name of the attack test run
NAME=$2


# ssh info for the remote test laptop
TL_USERNAME=sdmay23-16
TL_HOST=10.26.55.73

# ssh info for the ML server
MLS_USERNAME=sdmay23_16
MLS_HOST=berk.ece.iastate.edu

#########
# START #
#########

cd ${SOURCE_DIR}
scp $SOURCE_DIR$NAME/X_attack_test_15.csv ${MLS_USERNAME}@${MLS_HOST}:~/testing_workspace/Data/
ssh -l ${MLS_USERNAME} ${MLS_HOST} "cd testing_workspace/; source tensorflow/roy-venv/bin/activate; ./Restored_model_test.py >> results_${NAME}.txt; deactivate"
scp ${MLS_USERNAME}@${MLS_HOST}:~/testing_workspace/results_${NAME}.txt ${SOURCE_DIR}/${NAME}/results.txt