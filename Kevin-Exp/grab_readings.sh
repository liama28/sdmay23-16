#!/bin/bash

# Required $# to have 1 arg
if [ "$#" -ne 1 ]; then
	echo "Please provide a name for the output text file"
	exit
fi

scp sdmay23-16@10.26.52.121:/home/sdmay23-16/Kevin_Test/spectre-attack/power_readings.txt power_readings.txt

if [[ "$1" != *.txt ]]; then
	FILENAME="${1}.txt"
else
	FILENAME="$1"
fi

awk '{print NR  "," $s}' power_readings.txt > $FILENAME
mv $FILENAME pwr_txt/
rm power_readings.txt
