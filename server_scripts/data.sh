#!/bin/bash

#start_time=$(date +%s)
# Cored
for i in {1..5001};
do
  echo $(cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/intel-rapl\:0\:0/energy_uj) >> spectre_data_test.txt 
done





