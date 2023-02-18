#!/bin/bash
#sh scp_helper.sh ~/Desktop/Senior_Design/sdmay23-16/Liam_experiments/ Source_test.c testrun3423 3 1

#############
# ARGUMENTS #
#############
# Working directory / source directory
SOURCE_DIR=$1
# Source file for the attack. Relative to the source directory
SOURCE_FILE=$2
# Name of the attack test run
NAME=$3
# Number of times to run the attack
RUNS=$4
# Wait time between each attack for simple attack runs
WAIT_TIME=$5
# 0 or 1. 0 = Collect data for the ML model. 1 = run a simple attack
TEST=$6

# ssh info for the remote test laptop
TL_USERNAME=sdmay23-16
TL_HOST=10.26.55.93

# ssh info for the ML server
MLS_USERNAME=sdmay23_16
MLS_HOST=berk.ece.iastate.edu

# Grab file name from source file.
#(ex: basename /attack_code/spectre/Source.c = Source.c)
FILE_NAME="$(basename -- $SOURCE_FILE)"
#########
# START #
#########

cd ${SOURCE_DIR}
mkdir ${NAME}
# Copy source code to remote test laptop
ssh -l ${TL_USERNAME} ${TL_HOST} "mkdir ~/testing_workspace/${NAME}"
scp $SOURCE_DIR$SOURCE_FILE ${TL_USERNAME}@${TL_HOST}:~/testing_workspace/${NAME}/$FILE_NAME
ssh -l ${TL_USERNAME} ${TL_HOST} "sudo ~/testing_workspace/run_attack.sh ${FILE_NAME} ${NAME} ${RUNS} ${WAIT_TIME} ${TEST}"
scp -r ${TL_USERNAME}@${TL_HOST}:~/testing_workspace/${NAME} ${SOURCE_DIR}