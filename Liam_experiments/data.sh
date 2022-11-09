#!/bin/bash
echo "START POWER DATA COLLECTION:" $(date +"%H:%M:%S");
for ((i=1; i<=${1}; i++));
do
    echo $(cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/intel-rapl\:0\:0/energy_uj)
done
echo "END POWER DATA COLLECTION:" $(date +"%H:%M:%S");
