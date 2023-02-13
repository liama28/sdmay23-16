#!/bin/bash
#sudo ./run_attack.sh Source_test.c testrun1 3 1

#############
# ARGUMENTS #
#############
# .c source code file of attack. Located in /home/sdmay23-16/testing_workspace/{NAME}/
SOURCE_FILE=$1
# This name will be used to distinguish the attack run. Default will use a time stamp
NAME=$2
# Number of times to run the attack
RUNS=$3
# Time between runs (seconds)
WAIT_TIME=$4
# 0 or 1. 0 = Collect data for the ML model. 1 = run a simple attack
TEST=$5

#########
# START #
#########
cd /home/sdmay23-16/testing_workspace

NUM_PROC=$(ps -ef | grep run_attack.sh | wc -l)
if [ $((NUM_PROC)) -gt 3 ]; then
    echo "Detected attack already running. Quitting run..."
    exit 1;
fi

gcc -o ${NAME}/out.o -std=c99 ${NAME}/${SOURCE_FILE} 2> ${NAME}/gcc.txt

echo "START OF ATTACKS" $(date +"%H:%M:%S") >> ${NAME}/log.txt

################
# ML model run #
################
if [ $5 -eq 0 ]
then
  for ((i=1; i<=${RUNS}; i++));
  do
    sudo ./data_spec.sh 5001 "${NAME}/data_${i}.txt" &
    rm -f ${NAME}/out.o
    gcc -o ${NAME}/out.o -std=c99 ${NAME}/${SOURCE_FILE}
    ./${NAME}/out.o
    wait
    sleep 5s
    echo "${i}"
  done

#####################
# Simple attack run #
#####################
else
  sudo ./data_kill.sh >> "${NAME}/data.txt" &
  sleep 1
  _pid=$(ps --ppid $! -o pid=)
  #./clock_speed.sh >> "${NAME}/clock_speed_${NAME}.txt" &
  #_pid_clock_speed=$!
  echo "PID: ${_pid}" >> ${NAME}/log.txt
  for ((i=1; i<=${RUNS}; i++));
  do
    echo "START ATTACK ${i}" $(date +"%H:%M:%S") >> ${NAME}/log.txt
    time ./${NAME}/out.o >> ${NAME}/log.txt 
    echo "END ATTACK ${i}" $(date +"%H:%M:%S") >> ${NAME}/log.txt
    sleep ${WAIT_TIME}
  done
  sudo kill -SIGUSR1 ${_pid}
  #sleep 1
  #sudo kill ${_pid_clock_speed}
fi

echo "END OF ATTACKS" $(date +"%H:%M:%S") >> ${NAME}/log.txt



