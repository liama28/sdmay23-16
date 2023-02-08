#!/bin/bash
finished=0
trap 'finished=1' SIGUSR1
while ! ((finished))
do
    ./${1}
done