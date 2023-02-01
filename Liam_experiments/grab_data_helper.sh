#!/bin/bash

#sh grab_data_helper.sh ~/Desktop/Senior_Design/sdmay23-16/Liam_experiments/ Source_test.c testrun3423 3 1

SOURCE_DIR=$1

SOURCE_FILE=$2

NAME=$3

RUNS=$4

WAIT_TIME=$5

USERNAME=sdmay23-16

HOST=10.26.48.7

cd ${SOURCE_DIR}

mkdir ${NAME}

scp $SOURCE_DIR$SOURCE_FILE ${USERNAME}@${HOST}:~/Liam_dir/${NAME}.c

ssh -l ${USERNAME} ${HOST} "sudo ~/Liam_dir/run_attack.sh ${NAME}.c ${NAME} ${RUNS} ${WAIT_TIME}"

scp -r ${USERNAME}@${HOST}:~/Liam_dir/${NAME} ${SOURCE_DIR}
