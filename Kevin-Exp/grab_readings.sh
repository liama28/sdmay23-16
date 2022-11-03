#!/bin/bash

scp sdmay23-16@10.26.52.121:/home/sdmay23-16/Kevin_Test/spectre-attack/power_readings.txt power_readings.txt
awk '{print NR  "," $s}' power_readings.txt > pwr_input.txt
rm power_readings.txt
