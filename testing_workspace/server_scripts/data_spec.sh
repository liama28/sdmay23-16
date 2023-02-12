#!/bin/bash
for ((i=1; i<=${1}; i++))
do
    echo $(cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/intel-rapl\:0\:0/energy_uj) >> ${2}
    #sleep 0.0005
done
