#!/bin/bash
finished=0
i=0
trap 'finished=1' SIGINT       
trap 'echo "$i" >> ${1}/int.txt' SIGUSR1 
while ! ((finished))
do
    ((i++))
    echo $(cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/intel-rapl\:0\:0/energy_uj) >> ${1}/data.txt
    #sleep 0.0005
done
 