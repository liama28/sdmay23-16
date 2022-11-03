#!/bin/bash

#start_time=$(date +%s)
# Cored
temp=${/sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/intel-rapl\:0\:0/energy_uj}
for i in {1..5001};
do
  temp2=${/sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/intel-rapl\:0\:0/energy_uj}
  echo temp2-temp1
