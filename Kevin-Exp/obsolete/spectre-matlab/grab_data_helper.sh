#!/bin/bash

#sh grab_data_helper.sh ~/Desktop/Senior_Design/sdmay23-16/Liam_experiments/ Source_test.c testrun3423 3 1

SOURCE_DIR=$1

SOURCE_FILE=$2

NAME=$3

RUNS=$4

WAIT_TIME=$5

USERNAME=sdmay23-16

HOST=10.26.52.121

cd ${SOURCE_DIR}

mkdir ${NAME}
 
scp -i ~/.ssh/id_sdmay23_rsa $SOURCE_DIR$SOURCE_FILE ${USERNAME}@${HOST}:~/Kevin_Test/spectre-attack/${NAME}.c

ssh -i ~/.ssh/id_sdmay23_rsa -l ${USERNAME} ${HOST} "sudo ~/Kevin_Test/spectre-attack/run_attack.sh ${NAME}.c ${NAME} ${RUNS} ${WAIT_TIME}"

scp -i ~/.ssh/id_sdmay23_rsa -r ${USERNAME}@${HOST}:~/Kevin_Test/spectre-attack/${NAME} ${SOURCE_DIR}
