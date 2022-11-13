#!/bin/bash
finished=0
trap 'finished=1' SIGUSR1
while ! ((finished))
do
    echo $(cat /sys/devices/virtual/powercap/intel-rapl/intel-rapl\:0/intel-rapl\:0\:0/energy_uj)
done
