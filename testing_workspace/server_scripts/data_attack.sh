#!/bin/bash

# ./data.sh &
# ./attack.sh

for j in {1..20};
do
  sudo ./data.sh &
  ./attack.sh 
  wait
  sleep 5s
done
