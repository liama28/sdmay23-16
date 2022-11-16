#!/bin/bash
while :
 do
  lscpu | grep "CPU MHz:" | awk -F " " '{print $3}'
  sleep 0.05
done
