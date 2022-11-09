#!/bin/bash
#sh ssh_grab_data.sh ~/Desktop/Senior_Design/sdmay23-16/Liam_experiments/ /home/sdmay23-16/Liam_dir/ Source_test.c

#Directory on host machine with attack c file and where output data text file will go
#SOURCE_DIR=~/Desktop/Senior_Design/
#First argument will be the source directory
SOURCE_DIR=$1

#Directory on server where temp files and copy of the data and attack will go
#DEST_DIR=/home/sdmay23-16/Liam_dir/
#Sencond argument will be the destination directory
DEST_DIR=$2

#File name of attack code
#FILENAME=Source_test.c
#Third argument will be the filename located in source directory
FILENAME=$3

#Username for server
USERNAME=sdmay23-16

#Server IP address or hostname
HOST=10.26.52.121

#Where the power data script is at. Must be this instance because the server is configed to allow it to run with sudo
DATASCRIPT=/home/sdmay23-16/Liam_dir/data.sh

#Name that will be used for output and copy of c file
TIMESTAMP=$(date +"%Y%m%dT%H%M%S");



#Copy Attack code onto server
scp $SOURCE_DIR$FILENAME ${USERNAME}@${HOST}:${DEST_DIR}/${TIMESTAMP}.c
#scp ~/Desktop/Senior_Design/Source_test.c sdmay23-16@10.26.52.121:/home/sdmay23-16/Liam_dir/temp.c

#Run attack code on server and generate output
ssh -l ${USERNAME} ${HOST} "cd ${DEST_DIR}; gcc -o temp.o ${TIMESTAMP}.c; ./temp.o & sudo ${DATASCRIPT} >> ${TIMESTAMP}.txt"

#Grab output
scp ${USERNAME}@${HOST}:${DEST_DIR}${TIMESTAMP}.txt ${SOURCE_DIR}/${TIMESTAMP}.txt
#scp sdmay23-16@10.26.52.121:/home/sdmay23-16/Liam_dir/temp.txt ~/Desktop/Senior_Design/powerdata_output.txt
