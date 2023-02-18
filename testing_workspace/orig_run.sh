#!/bin/bash

SOURCE_DIR=$1
SOURCE_FILE=$2

USERNAME=sdmay23-16
HOST=10.26.55.93

cd ${SOURCE_DIR}
rm spectre_data_test.txt
touch spectre_data_test.txt
scp $SOURCE_DIR$SOURCE_FILE ${USERNAME}@${HOST}:~/testing_workspace/Source.c
scp $SOURCE_DIR/spectre_data_test.txt ${USERNAME}@${HOST}:~/testing_workspace/spectre_data_test.txt
ssh -l ${USERNAME} ${HOST} "cd ~/testing_workspace/; sudo ./data_attack.sh"
scp -r ${USERNAME}@${HOST}:~/testing_workspace/spectre_data_test.txt ${SOURCE_DIR}
