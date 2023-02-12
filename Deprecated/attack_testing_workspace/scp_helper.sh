#!/bin/bash

#sh scp_helper.sh ~/Desktop/Senior_Design/sdmay23-16/Liam_experiments/ Source_test.c testrun3423 3 1

SOURCE_DIR=$1
SOURCE_FILE=$2
NAME=$3
RUNS=$4
WAIT_TIME=$5
MODEL=$6

USERNAME=sdmay23-16
HOST=10.26.48.7

cd ${SOURCE_DIR}
mkdir ${NAME}
scp $SOURCE_DIR$SOURCE_FILE ${USERNAME}@${HOST}:~/testing_workspace/${NAME}.c
if [ $6 -eq 0 ]
then 
    ssh -l ${USERNAME} ${HOST} "sudo ~/testing_workspace/run_attack.sh ${NAME}.c ${NAME} ${RUNS} ${WAIT_TIME}"
else
    ssh -l ${USERNAME} ${HOST} "sudo ~/testing_workspace/run_attack_model.sh ${NAME}.c ${NAME} ${RUNS}"
fi
scp -r ${USERNAME}@${HOST}:~/testing_workspace/${NAME} ${SOURCE_DIR}
