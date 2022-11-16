#!/bin/bash
#sudo ./run_attack.sh Source_test.c testrun1 3 1

# .c source code file of attack. Located in /home/sdmay23-16/Liam_dir
SOURCE_FILE=$1

# This name will be used to distinguish the attack run. Probably will use a time stamp
NAME=$2

# Number of times to run the attack
RUNS=$3

# Time between runs (seconds)
WAIT_TIME=$4

cd /home/sdmay23-16/Liam_dir

if [ -d ${NAME} ]
then
    echo "Directory ${NAME} exists. Quiting attack.."; exit 1;
fi

mkdir ${NAME}

gcc -o ${NAME}/${NAME}.o ${SOURCE_FILE} 2> ${NAME}/gcc_${NAME}.txt

echo "START OF ATTACKS" $(date +"%H:%M:%S") >> ${NAME}/log_${NAME}.txt

sudo ./data.sh >> "${NAME}/data_${NAME}.txt" &
sleep 1
_pid=$(ps --ppid $! -o pid=)

#./clock_speed.sh >> "${NAME}/clock_speed_${NAME}.txt" &

#_pid_clock_speed=$!

echo "PID: ${_pid}" >> ${NAME}/log_${NAME}.txt

for ((i=1; i<=${RUNS}; i++));
do
  echo "START ATTACK ${i}" $(date +"%H:%M:%S") >> ${NAME}/log_${NAME}.txt
  ./${NAME}/${NAME}.o >> ${NAME}/log_${NAME}.txt
  echo "END ATTACK ${i}" $(date +"%H:%M:%S") >> ${NAME}/log_${NAME}.txt
  sleep ${WAIT_TIME}
done

echo "END OF ATTACKS" $(date +"%H:%M:%S") >> ${NAME}/log_${NAME}.txt

sudo kill -SIGUSR1 ${_pid}

#sleep 1

#sudo kill ${_pid_clock_speed}
