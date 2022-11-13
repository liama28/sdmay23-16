#!/usr/bin/bash
finished=0
trap 'finished=1;echo Signal' SIGUSR1
while ! ((finished))
do
    sleep 5
    echo sleeping
done
echo done
