#!/bin/bash
#sudo ./run_attack.sh Source_test.c testrun1 3 1

# .c source code file of attack. Located in /home/sdmay23-16/Liam_dir
SOURCE_FILE=$1

# This name will be used to distinguish the attack run. Probably will use a time stamp
NAME=$2

# Number of times to run the attack
RUNS=$3

cd /home/sdmay23-16/testing_workspace

if [ -d ${NAME} ]
then
    echo "Directory ${NAME} exists. Quiting attack.."; exit 1;
fi

mkdir ${NAME}

gcc -o ${NAME}/${NAME}.o ${SOURCE_FILE} 2> ${NAME}/gcc_${NAME}.txt

for ((i=1; i<=${RUNS}; i++));
do
echo "START OF ATTACK ${i}" $(date +"%H:%M:%S") >> ${NAME}/log_${NAME}.txt
./run_indef.sh ${NAME}/${NAME}.o >> ${NAME}/log_${NAME}.txt &
sleep 1
_pid=$!
sudo ./data_spec.sh 5001 >> "${NAME}/data_${i}.txt"
sudo kill -SIGUSR1 ${_pid}
echo "KILLED PID: ${_pid}" >> ${NAME}/log_${NAME}.txt
echo "END OF ATTACK ${i}" $(date +"%H:%M:%S") >> ${NAME}/log_${NAME}.txt
echo "${i}"
done